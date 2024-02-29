import mysql.connector

def connect(con_type):

    # con_type is a number specifying reader or inserter
    # These users have different permissions so user the right one

    if con_type == 0:
        user = "Label_Reader"
    elif con_type == 1:
        user = "Label_Inserter"

    cnx = mysql.connector.connect(
        user=user,
        password="password",
        database="HGCAL_Labeling"
    )

    return cnx
