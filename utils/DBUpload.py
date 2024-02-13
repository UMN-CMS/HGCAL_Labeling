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
            print("Row present for {}, skipping insert".format(name))
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

            sql = "SELECT sub_type_id FROM Sub_Type WHERE sub_sn = %s"
            val = (sub_sn,)

            cur.execute(sql, val)
        
            try:
                results = cur.fetchall()
                sub_id = results[0][0]
                print("Row present for {}, skipping insert".format(name))
            except:
                print("No row present for {}, will add into Major_Type table".format(name))
                sql = "INSERT INTO Sub_Type (name, sub_sn, sub_code, identifier_name, digits) VALUES (%s, %s, %s, %s, %s)"
                val = (name, sub_sn, sub_code, identifier, digits)

                cur.execute(sql, val)
                cnx.commit()

                print(cur.rowcount, "record inserted into Sub_Type with name {}".format(name))

            sql = "SELECT major_type_id FROM Major_Type WHERE major_sn = %s"
            val = (major_sn,)

            cur.execute(sql, val)
            maj_id = cur.fetchall()[0][0]

            sql = 'SELECT sub_type_id FROM Sub_Type WHERE sub_sn = %s'
            val = (sub_sn,)

            cur.execute(sql, val)
            sub_id = cur.fetchall()[0][0]

            sql = "SELECT * from Major_Sub_Stitch WHERE major_type_id = %s and sub_type_id = %s"
            val = (maj_id, sub_id)

            cur.execute(sql, val)

            try:
                val = cur.fetchall()[0][0]
                print("Entry present in stitch table ({},{}), skipping insert".format(maj_id, sub_id))
                continue
            except:

                sql = "INSERT INTO Major_Sub_Stitch (major_type_id, sub_type_id) VALUES (%s, %s)"
                val = (maj_id, sub_id)

                cur.execute(sql, val)
                cnx.commit()

def upload_label(label, cnx):

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

    def check_sub(sub, cur):

        sql = "SELECT sub_type_id FROM Sub_Type WHERE sub_code = %s"
        val = (sub,)
    
        cur.execute(sql, val)
        try:
            sub_type_id = cur.fetchall()[0][0]
            return True, sub_type_id
        except:
            return False, -1

    cur = cnx.cursor()

    prefix = label[:3]
    major = label[3:5]

    print(label)
    temp_three_sub = label[5:8]
    temp_four_sub = label[5:9]
    three_sub = False
    four_sub = False

    is_three_sub, sub_type_id = check_sub(temp_three_sub, cur)
    is_four_sub, sub_type_id = check_sub(temp_three_sub, cur)


    if is_three_sub:
        sub = temp_three_sub
        sn = label[8:]
    if is_four_sub:
        sub = temp_four_sub
        sn = label[9:]

    major_type_id = match_major(major, cur)
    if major_type_id == -1:
        print("Cannot find major type {} for sn={}".format(major, label))
        return

    if three_sub and four_sub:
        print("Conflicting three and four character subtype, cannot resolve ({},{})".format(temp_three_sub, temp_four_sub))
        return
    elif not three_sub and not four_sub:
        print("No mathcing subtype for {} or {}".format(temp_three_sub, temp_four_sub))
        return
    
    print(prefix, major, sub, sn, major_type_id, sub_type_id)

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("--input", type=str, default="../static/printed_barcodes.json", help="Name of input file with printed barcodes")
    parser.add_argument("--updateMeta", type=bool, default=False, help="Update major type and subtype tables (default=False)")

    args = parser.parse_args()

    label_dict = load_labels(args.input)

    cnx = connect(1)

    if args.updateMeta:
        update_metatables(cnx, majortypes)

    for l in label_dict.keys():
        
        if l[:4] == "3205": continue

        upload_label(l, cnx)

