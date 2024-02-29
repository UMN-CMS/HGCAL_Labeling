from argparse import ArgumentParser
import json
import sys

sys.path.append("../static")

from MajorTypes import majortypes
from connect import connect

def load_labels(inpath):

    with open(inpath, "r") as f:
        label_dict = json.load(f)

    f.close()

    return label_dict

def update_metatables(cnx, majortypes):
   
    print("\nChecking for new major types and subtypes:\n")

    # Make an orphan category for Major and Sub type to house lost labels
    cur = cnx.cursor()

    sql = "SELECT major_type_id FROM Major_Type WHERE name='ORPHAN'"
    cur.execute(sql)

    try:
        cur.fetchall()[0][0]
    except:
        print("Adding ORPHAN major type identified by major_sn={} and major_code={}".format(99, "XX"))
        sql = "INSERT INTO Major_Type (name, major_sn, major_code) VALUES (%s, %s, %s)"
        val = ("ORPHAN", "99", "XX")

        cur.execute(sql, val)

        cnx.commit()
   
    sql = "SELECT sub_type_id FROM Sub_Type WHERE name='ORPHAN'"
    cur.execute(sql)

    try:
        cur.fetchall()[0][0]
    except:
        print("Adding ORPHAN sub type identified by sub_sn={} and sub_code={}".format(9999, "XXXX"))
        sql = "INSERT INTO Sub_Type (name, sub_sn, sub_code, digits, identifier_name) VALUES (%s, %s, %s, %s, %s)"
        val = ("ORPHAN", "9999", "XXXX", "4", "ORPHAN")

        cur.execute(sql, val)
   
        cnx.commit()
     

    for key in majortypes:
    
        major_code = majortypes[key]["major_code"]
        major_sn = str(majortypes[key]["major_sn"]) if len(str(majortypes[key]["major_sn"])) == 2 else "0" + str(majortypes[key]["major_sn"])
        name = key
        if major_code == '': continue

        cur = cnx.cursor()

        sql = "SELECT major_type_id FROM Major_Type WHERE major_sn = %s"
        val = (major_sn,)

        cur.execute(sql, val)
       
        try:
            results = cur.fetchall()
            maj_id = results[0][0]
            #print("Row present for {}, skipping insert".format(name))
        except:
            print("No row present for {}, will add into Major_Type table".format(name))
            sql = "INSERT INTO Major_Type (name, major_sn, major_code) VALUES (%s, %s, %s)"
            val = (name, major_sn, major_code)

            cur.execute(sql, val)
            cnx.commit()

            print(cur.rowcount, "record inserted into Major_Type with name {}".format(name))

        sql = "SELECT major_type_id FROM Major_Type WHERE major_sn = %s"
        val = (major_sn,)

        if majortypes[key]["subtypes"] == None:
            print("No subtype associated with {}".format(key))
            continue

        for sub_key, info in majortypes[key]["subtypes"].items():
 
            if "name" not in info.keys():
                name = sub_key
                identifier = sub_key
            else:
                name = info["name"]
                identifier = sub_key

            sub_code = info["sub_code"]
            sub_sn = info["sub_sn"]
            digits = len(sub_code)

            sql = "SELECT sub_type_id FROM Sub_Type WHERE sub_sn = %s and sub_code = %s"
            val = (sub_sn, sub_code)

            cur.execute(sql, val)
        
            try:
                results = cur.fetchall()
                sub_id = results[0][0]
                #print("Row present for {}, skipping insert".format(name))
            except:
                print("No row present for {}, will add into Sub_Type table".format(name))
                sql = "INSERT INTO Sub_Type (name, sub_sn, sub_code, identifier_name, digits) VALUES (%s, %s, %s, %s, %s)"
                val = (name, sub_sn, sub_code, identifier, digits)

                cur.execute(sql, val)
                cnx.commit()

                print(cur.rowcount, "record inserted into Sub_Type with name {}".format(name))

            sql = "SELECT major_type_id FROM Major_Type WHERE major_sn = %s"
            val = (major_sn,)

            cur.execute(sql, val)
            maj_id = cur.fetchall()[0][0]

            sql = 'SELECT sub_type_id FROM Sub_Type WHERE sub_code = %s and sub_sn = %s'
            val = (sub_code, sub_sn)

            cur.execute(sql, val)
            sub_ids = cur.fetchall()

            for sub in sub_ids:
                sub_id = sub[0]

                sql = "SELECT * from Major_Sub_Stitch WHERE major_type_id = %s and sub_type_id = %s"
                val = (maj_id, sub_id)

                cur.execute(sql, val)

                try:
                    val = cur.fetchall()[0][0]
                    #print("Entry present in stitch table ({},{}), skipping insert".format(maj_id, sub_id))
                    continue
                except:

                    sql = "INSERT INTO Major_Sub_Stitch (major_type_id, sub_type_id) VALUES (%s, %s)"
                    val = (maj_id, sub_id)

                    cur.execute(sql, val)
                    cnx.commit()

def upload_label(label, cnx, f):

    def match_major(maj, cur):
        
        sql = "SELECT major_type_id FROM Major_Type WHERE major_code = %s"
        val = (maj,)
        
        cur.execute(sql, val)
        try:
            major_type_id = cur.fetchall()[0][0]
            return major_type_id
        except:
            sql = "SELECT major_type_id FROM Major_Type WHERE major_sn = %s"
            val = (maj,)
            
            cur.execute(sql, val)
            try:
                major_type_id = cur.fetchall()[0][0]
                return major_type_id
            except:
                return -1 

    def check_sub(sub, maj_id, cur):

        sql = "SELECT sub_type_id FROM Sub_Type WHERE sub_code = %s OR sub_sn = %s"
        val = (sub, sub)
    
        cur.execute(sql, val)
        try:
            sub_type_id = cur.fetchall()
            sub_type_id[0]
            for i,sub_id in enumerate(sub_type_id):
                if check_stitch(maj_id, sub_id[0]):
                    return True, sub_type_id[i][0]
            return False, -2
        except:
            return False, -1

    def check_stitch(maj_id, sub_id):
        
        sql = "SELECT * from Major_Sub_Stitch WHERE major_type_id = %s AND sub_type_id = %s"
        val = (maj_id, sub_id)

        cur.execute(sql, val)
        try:
            cur.fetchall()[0]
            return True
        except:
            return False

    cur = cnx.cursor()
    offset = 0

    if "3205" == label[:4]:
        return
        prefix = label[:4]
        offset = 1

    prefix = label[:3+offset]
    major = label[3+offset:5+offset]

    major_type_id = match_major(major, cur)

    temp_two_sub = label[5+offset:7+offset]
    temp_three_sub = label[5+offset:8+offset]
    temp_four_sub = label[5+offset:9+offset]

    is_two_sub, two_sub_type_id = check_sub(temp_two_sub, major_type_id, cur)
    is_three_sub, three_sub_type_id = check_sub(temp_three_sub, major_type_id, cur)
    is_four_sub, four_sub_type_id = check_sub(temp_four_sub, major_type_id, cur)


    if is_three_sub:
        sub = temp_three_sub
        sub_type_id = three_sub_type_id
        sn = label[8+offset:]
    elif is_four_sub:
        sub = temp_four_sub
        sub_type_id = four_sub_type_id
        sn = label[9+offset:]
    elif is_two_sub:
        sub = temp_two_sub
        sub_type_id = two_sub_type_id
        sn = label[7+offset:]
    else:
        sn = label[9+offset:]
        sub = temp_four_sub
        sub_type_id = four_sub_type_id

    if major_type_id < 0 or sub_type_id < 0:
        print("Cannot find major type {} or sub type {} for sn={}".format(major, sub, label))
        print("Will continue as orphan label upload")

        f.write(label + "\n")

        major = "XX"
        sub = "XXXX"


    elif not is_two_sub and not is_three_sub and not is_four_sub:
        print("No mathcing subtype for {} or {} or {}".format(temp_two_sub, temp_three_sub, temp_four_sub))

        f.write(label + "\n")

        major = "XX"
        sub = "XXXX"
   
    pass_stitch = check_stitch(major_type_id, sub_type_id)
 
    print(prefix, major, sub, sn, major_type_id, sub_type_id, pass_stitch)

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("--input", type=str, default="../static/printed_barcodes.json", help="Name of input file with printed barcodes")
    parser.add_argument("--updateMeta", action="store_true", default=False, help="Update major type and subtype tables (default=False)")
    parser.add_argument("--loadLabels", action="store_true", default=False, help="Load labels into DB for JSON file")

    args = parser.parse_args()

    label_dict = load_labels(args.input)

    cnx = connect(1)

    if args.updateMeta:
        update_metatables(cnx, majortypes)

    if args.loadLabels:

        with open("./Orphan_Labels.txt", "w") as f:

            for l in label_dict.keys():
                
                upload_label(l, cnx, f)

        f.close()
