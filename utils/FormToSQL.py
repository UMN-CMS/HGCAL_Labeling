"""
HGCAL_Labeling, University of Minnesota, Spring 2024
Riley Passe

Brief Description:
This code pulls down user input from the google form into csv format, converts
the data into the correct format with correct label coding, and then uploads 
new entries to the MySQL server.

Executable at bottom of file.
"""
import pandas as pd
import mysql.connector
import os.path
import csv
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def download_csv(service, spreadsheet_id, range_name, output_file):
    """
    Downloads spreadsheet from google forms as CSV.
    """
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(values)

        print(f"CSV file has been downloaded to {output_file}")

    except HttpError as err:
        print(err)


def main_dl(SCOPES, SPREADSHEET_ID, RANGE_NAME):
    """
    Pulls down spreadsheet from google forms. Results in RawForm.csv.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        download_csv(service, SPREADSHEET_ID, RANGE_NAME, "RawForm.csv")

    except HttpError as err:
        print(err)


def edit_csv(raw_csv_file, reviewed_csv_file, row_number, connection):
    """
    Takes row_number row of raw_csv_file, allows user to edit it in command line,
    then adds it to reviewed_csv_file in format to be uploaded to SQL.
    """
    raw_df = pd.read_csv(raw_csv_file)
    reviewed_csv = pd.read_csv(reviewed_csv_file)
    
    # Extract the row to edit
    row_to_edit = raw_df.iloc[row_number]

    sn = row_to_edit["Serial number generation"]

    print("Editing Row Number:", row_number, ", Serial Number:", sn)
    print("Row Content:")

    for column, value in row_to_edit.items():
        print(f"{column}: {value}")

    #Check if user wants to edit
    if to_edit():
        #Edit then save to reviewed
        edited_row = {}
        for column in row_to_edit.index:
            value = row_to_edit[column]
            new_value = input(f"Edit {column} [{value}] (Press enter to skip): ")
            if new_value != '':
                edited_row[column] = new_value
                print(f"{column} edited.")
            else:
                edited_row[column] = value

        
        # Add the edited row to the reviewed DataFrame
        reviewed_csv = reviewed_csv._append(edited_row, ignore_index=True)
        
        # Save the reviewed DataFrame to the CSV file
        reviewed_csv.to_csv(reviewed_csv_file, index=False)
    else: 
        #Just save to reviewed
        reviewed_csv = reviewed_csv._append(row_to_edit, ignore_index=True)

    reviewed_csv.to_csv(reviewed_csv_file, index=False)

    print() #spacing in case of error message

    conn_mysql = connection()
    cursor = conn_mysql.cursor()

    #removes Null values which crash SQL
    reviewed_csv = reviewed_csv.where(pd.notnull(reviewed_csv), None)

    #Replaces major type with its 2 letter code
    reviewed_csv.iloc[row_number,6] = extract_string(reviewed_csv.iloc[row_number,6])

    #Convert major and sub id into their numerical codes
    major_id = get_major_id(reviewed_csv, cursor)
    get_sub_id(reviewed_csv, major_id, cursor)

    #final save
    reviewed_csv.to_csv(reviewed_csv_file, index=False)
    print("Row added to reviewed csv.")
    print()


def find_unreviewed_indices(raw_csv_file, reviewed_csv_file):
    """
    Gives indicies of rows with serial numbers that are in raw_csv_file 
    but are not in reviewed_csv_file
    """
    raw_csv = pd.read_csv(raw_csv_file)
    if not os.path.exists(reviewed_csv_file):
        columns = ['Timestamp', 'Email Address', 'Orderer Name', 'Orderer Email Address', 'Institution Name',
                   'Shipping Address', 'Component Major Type', 'Subtype', 'Number of Labels',
                   'Special Requests/Constraints', 'Desired Receive Date', 'Serial number generation']
        reviewed_csv = pd.DataFrame(columns=columns)
        reviewed_csv.to_csv(reviewed_csv_file, index=False)
    else:
        reviewed_csv = pd.read_csv(reviewed_csv_file)
    serial_number_column = "Serial number generation" if "Serial number generation" in raw_csv.columns else None
    
    if serial_number_column is None:
        raise ValueError("Column 'Serial number generation' not found in the raw input CSV.")
    
    reviewed_serial_numbers = set(reviewed_csv[serial_number_column])
    unreviewed_row_indices = raw_csv[~raw_csv[serial_number_column].isin(reviewed_serial_numbers)].index
    
    return unreviewed_row_indices


def to_edit():
    """
    Asks user if they would like to edit. Returns bool.
    """
    while True:
        to_edit = input("Would you like to edit? [y,N]: ").lower()
        if to_edit in {'y', 'yes'}:
            return True
        elif to_edit in {'', 'n', 'no'}:
            return False
        else:
            print("Invalid input. [y,N]: ")


def extract_string(input_string):
    """
    Extracts string between "(" and ")".
    """
    # Define a regular expression pattern to match the string within parentheses
    pattern = r'\((.*?)\)'
    
    # Use re.search() to find the first occurrence of the pattern in the input string
    match = re.search(pattern, input_string)
    
    # If match is found, return the string within parentheses
    if match:
        return match.group(1)
    else:
        return None


def get_major_id(reviewed_csv, cursor):
    """
    Gets major id number from sql database. Requests user input if not found.
    """
    is_invalid = False
    while True:
        try:
            major_comp = reviewed_csv.iloc[row_number,6]
            if is_invalid:
                    major_comp = None
            if major_comp is None:
                while True:
                    name = reviewed_csv.iloc[row_number, 2]
                    order_date = reviewed_csv.iloc[row_number, 0]  
                    code = input(f"Major type not found for {name}, {order_date}. Please provide a 2-letter code: ").strip().upper()
                    if len(code) == 2:
                        major_comp = code
                        break
                    else:
                        print("Invalid code. Please provide a 2-letter code.")

            get_major_id_query = "SELECT major_type_id FROM Major_Type WHERE major_code = %s"
            cursor.execute(get_major_id_query, (major_comp,))
            major_id = cursor.fetchone()
            if major_id:
                reviewed_csv.iloc[row_number, 6] = major_id[0]
                is_invalid = False
                break
            
            else:
                is_invalid = True
                # Ask user for code again
                continue  # Retry the loop
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Error occurred while executing MySQL query. Please try again.")
    return major_id


def get_sub_id(reviewed_csv, major_id, cursor):
    """
    Gets sub id number from sql database. Requests user input if not found.
    """
    found_sub = False
    #starting by splicing subtype input, checking those, then continuing if needed to user input
    sub_sub_comp_lst = reviewed_csv.iloc[row_number,7].split("-")
    for sub_sub_comp in sub_sub_comp_lst:
        try:
            get_sub_id_query = "SELECT sub_type_id FROM Sub_Type WHERE sub_code = %s"
            cursor.execute(get_sub_id_query, (sub_sub_comp,))
            sub_id1 = cursor.fetchone()
            if sub_id1:
                #Checking major/subtype compatability
                check_compat = "SELECT Sub_Type.sub_code FROM (Major_Sub_Stitch, Sub_Type) WHERE Major_Sub_Stitch.major_type_id = %s and Sub_Type.sub_type_id = %s"
                cursor.execute(check_compat, (major_id[0], sub_id1[0],))
                matching_id = cursor.fetchone()
                if matching_id == None:
                    continue
                reviewed_csv.iloc[row_number, 7] = sub_id[0]
                found_sub = True
                break
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Error occurred while executing MySQL query. Please try again.")

    #subtype id not found from splice, try whole then ask user
    if not found_sub:
    #getting subtype id number
        is_invalid2 = False
        while True:
            try:
                sub_comp = reviewed_csv.iloc[row_number,7]
                if is_invalid2:
                        sub_comp = None
                if sub_comp is None:
                    while True:
                        name = reviewed_csv.iloc[row_number, 2]
                        order_date = reviewed_csv.iloc[row_number, 0]  
                        code = input(f"Subtype not found for {name}, {order_date}. Please provide subtype code: ").strip().upper()
                        if len(code) != None:
                            sub_comp = code
                            break
                        else:
                            print("Invalid code. Please provide a valid subtype code.")

                get_sub_id_query = "SELECT sub_type_id FROM Sub_Type WHERE sub_code = %s"
                cursor.execute(get_sub_id_query, (sub_comp,))
                sub_id = cursor.fetchone()
                if sub_id:
                    #Checking major/subtype compatability
                    check_compat = "SELECT Sub_Type.sub_code FROM (Major_Sub_Stitch, Sub_Type) WHERE Major_Sub_Stitch.major_type_id = %s and Sub_Type.sub_type_id = %s"
                    cursor.execute(check_compat, (major_id[0], sub_id[0],))
                    matching_id = cursor.fetchone()
                    if matching_id == None:
                        print("Error, Major-type does not match with given sub-type.")
                        continue
                    reviewed_csv.iloc[row_number, 7] = sub_id[0]
                    is_invalid2 = False
                    break
                else:
                    is_invalid2 = True
                    # Ask user for code again
                    continue  # Retry the loop
            except Exception as e:
                print(f"Error occurred: {e}")
                print("Error occurred while executing MySQL query. Please try again.")
    return sub_id


def connection():
    """
    Contains MySQL connector values.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3867",
        database="HGCAL_Labeling"
    )
    return connection


def csv_to_sql(csv_file):
    """
    Intended to convert ReviewedForm.cvs into the format of the MySQL database,
    then uploads to database once finished.
    """
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
    df['request_date'] = pd.to_datetime(df['request_date'], errors='coerce').fillna(df['order_date'])
    
    # Replace 'NaN' values with None for SQL compatability
    df = df.where(pd.notnull(df), None)

    #Fixing date/time format
    df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['request_date'] = pd.to_datetime(df['request_date']).dt.strftime('%Y-%m-%d %H:%M:%S')

    filtered_csv_file = "filtered_" + csv_file
    df.to_csv(filtered_csv_file, index=False)

    #if new, uploads to mysql
    for row in df.values.tolist():
        order_date = row[0]
        email = row [1]
        name = row[2]
        orderer_email = row[3]
        location = row[4]
        shipping_address = row [5]
        major_type = row[6]
        sub_type = row[7]
        num_lab = row[8]
        request_date = row[9]

        # Check if entry with same name and order_date exists
        check_query = "SELECT * FROM Order_Info WHERE name = %s AND email = %s AND orderer_email = %s AND location = %s AND shipping_address = %s AND major_type_id = %s AND sub_type_id = %s AND num_labels = %s AND order_date = %s AND request_date = %s"
        cursor.execute(check_query, (name, email, orderer_email, location, shipping_address, major_type, sub_type, num_lab, order_date, request_date))
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


############################################################################### 


if __name__ == "__main__":
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    # The ID and range of the specific spreadsheet.
    SPREADSHEET_ID = "1Y_fhllebp5jrWqHVwADHX0AIzJudbHyHFT-iDteq8ow"
    RANGE_NAME = "Form Responses 1!A1:Z"

    main_dl(SCOPES, SPREADSHEET_ID, RANGE_NAME)
    unreviewed_row_indices = find_unreviewed_indices("RawForm.csv", "ReviewedForm.csv")
    print("There are", len(unreviewed_row_indices), "new rows.")
    for row_number in find_unreviewed_indices("RawForm.csv", "ReviewedForm.csv"):
        edit_csv("RawForm.csv", "ReviewedForm.csv", row_number, connection)
    csv_to_sql("ReviewedForm.csv")


#  #Check if user wants to edit
#     if to_edit():
#         #Edit then save to reviewed
#         edited_row = {}
#         for column in row_to_edit.index:
#             value = row_to_edit[column]
#             new_value = input(f"Edit {column} [{value}] (Press enter to skip): ")
#             if new_value != '':
#                 print(f"{column} edited.")
#                 if numpy.isnan(edited_row[column]):
#                     edited_row[column] = None
#                 else:
#                     edited_row[column] = new_value
#             else:
#                 print(edited_row[column])
#                 if numpy.isnan(edited_row[column]):
#                     edited_row[column] = None
#                 else:
#                     edited_row[column] = value
        
#         # Add the edited row to the reviewed DataFrame
#         reviewed_csv = reviewed_csv._append(edited_row, ignore_index=True)
#         # Save the reviewed DataFrame to the CSV file
#         reviewed_csv.to_csv(reviewed_csv_file, index=False)
#     else: 
#         edited_row = {}
#         for column in row_to_edit.index:
#             value = row_to_edit[column]
#             if numpy.isnan(edited_row[column]):
#                 edited_row[column] = None
#             else:
#                 edited_row[column] = value
#         #Just save to reviewed
#         reviewed_csv = reviewed_csv._append(edited_row, ignore_index=True)

#         reviewed_csv.to_csv(reviewed_csv_file, index=False)