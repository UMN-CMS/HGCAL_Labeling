import pandas as pd
import mysql.connector

def connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="HGCAL_Labeling"
    )
    return connection

def csv_to_sql(csv_file):
    df = pd.read_csv(csv_file)
    conn_mysql = connection()
    cursor = conn_mysql.cursor()

    needed_columns = ['Timestamp', 'Email Address', 'Orderer Name', 'Orderer Email Address', 
                      'Institution Name', 'Shipping Address', 'Component Major Type', 
                      'Subtype', 'Number of Labels', 'Desired Receive Date']

    df = pd.read_csv(csv_file, usecols=needed_columns)

    # Map CSV columns to MySQL table columns
    column_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Orderer Email': 'orderer_email',
        'Institution Name': 'location',
        'Shipping Address': 'shipping_address',
        'Major Type': 'major_type_id',
        'Subtype': 'sub_type_id',
        'Number of Labels': 'num_labels',
        'Timestamp': 'order_date',
        'Desired Receive Date': 'request_date'
    }

    #mapping csv to sql data
    df = df.rename(columns=column_mapping)

    # Replace empty instances of 'request_date' with None
    #df['request_date'] = pd.to_datetime(df['request_date'], errors='coerce').fillna(df['order_date'])

    # Replace 'NaN' values with None
    df = df.where(pd.notnull(df), None)

    #Fixing date/time format
    df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['request_date'] = pd.to_datetime(df['request_date']).dt.strftime('%Y-%m-%d %H:%M:%S')


    filtered_csv_file = "filtered_" + csv_file
    df.to_csv(filtered_csv_file, index=False)

    #if new, uploads to mysql
    for row in df.values.tolist():
        name = row[2]
        order_date = row[0]

        # Check if entry with same name and order_date exists
        check_query = "SELECT * FROM Order_Info WHERE name = %s AND order_date = %s"
        cursor.execute(check_query, (name, order_date))
        existing_entry = cursor.fetchone()
        cursor.fetchall()

        #Inserting if it doesn't exist already
        if not existing_entry:
            print("Inserting", name, order_date, "into mysql server.")
            insert_query = "INSERT INTO Order_Info (order_date, email, name, orderer_email, location, shipping_address, major_type_id, sub_type_id, num_labels, request_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, row)
            cursor.fetchall()

    conn_mysql.commit()
    conn_mysql.close()

    print("Data uploaded to MySQL successfully.")

    