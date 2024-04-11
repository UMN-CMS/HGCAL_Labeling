import pandas as pd
import os.path
import csv
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from CSVtoSQL import csv_to_sql
from CSVtoSQL import connection

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# The ID and range of your specific spreadsheet.
SPREADSHEET_ID = "1Y_fhllebp5jrWqHVwADHX0AIzJudbHyHFT-iDteq8ow"
RANGE_NAME = "Form Responses 1!A1:Z"
#CSV files
raw_csv_file = "raw_input.csv"  # Provide the path to your raw input CSV file
reviewed_csv_file = "reviewed_input.csv"  # Provide the path to your reviewed input CSV file

def download_csv(service, spreadsheet_id, range_name, output_file):
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

def main_dl():
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

def find_unreviewed_rows(raw_csv_file, reviewed_csv_file):
    """
    Gives rows with serial numbers that are in raw_csv_file 
    but are not in reviewed_csv_file
    """
    raw_csv = pd.read_csv(raw_csv_file)

    #checks of reviewed csv exists, creates one if not
    if not os.path.exists(reviewed_csv_file):
        columns = ['Timestamp', 'Email Address', 'Orderer Name', 'Orderer Email Address', 'Institution Name',
                   'Shipping Address', 'Component Major Type', 'Subtype', 'Number of Labels',
                   'Special Requests/Constraints', 'Desired Receive Date', 'Serial number generation']
        reviewed_csv = pd.DataFrame(columns=columns)
        reviewed_csv.to_csv(reviewed_csv_file, index=False)
    else:
        reviewed_csv = pd.read_csv(reviewed_csv_file)

    # Get the timestamp and name columns
    timestamp_column = "Timestamp" if "Timestamp" in raw_csv.columns else None
    name_column = "Orderer Name" if "Orderer Name" in raw_csv.columns else None
    
    if timestamp_column is None or name_column is None:
        raise ValueError("Timestamp or Orderer Name column not found in the raw input CSV.")
    
    # Create a set of tuples containing (timestamp, name) from reviewed CSV
    reviewed_entries = set(zip(reviewed_csv[timestamp_column], reviewed_csv[name_column]))
    
    # Filter unreviewed rows based on timestamp and name
    unreviewed_rows = raw_csv[
        ~raw_csv.apply(lambda row: (row[timestamp_column], row[name_column]) in reviewed_entries, axis=1)
    ]
    
    return unreviewed_rows


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

def edit_csv(raw_csv_file, reviewed_csv_file, row_number, connection):
    """
    Takes row_number row of raw_csv_file, allows user to edit it in command line,
    then adds it to reviewed_csv_file.
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
    while True:
        to_edit = input("Would you like to edit? [y,N]: ").lower()
        if to_edit in {'y', 'yes'}:
            edit_bool = True
            break
        elif to_edit in {'', 'n', 'no'}:
            edit_bool = False
            break
        else:
            print("Invalid input. [y,N]: ")

    if edit_bool:
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

    
    # reviewed_csv.loc[1, 'Component Major Type'] = reviewed_csv.loc[1, 'Component Major Type'].str.extract(r'\(([^)]+)\)')

    conn_mysql = connection()
    cursor = conn_mysql.cursor()

    reviewed_csv = reviewed_csv.where(pd.notnull(reviewed_csv), None)

    reviewed_csv.iloc[row_number,6] = extract_string(reviewed_csv.iloc[row_number,6])

    #getting major id number
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



    reviewed_csv.to_csv(reviewed_csv_file, index=False)
    print("Row added to reviewed csv.")
    print()

def extract_string(input_string):
    # Define a regular expression pattern to match the string within parentheses
    pattern = r'\((.*?)\)'
    
    # Use re.search() to find the first occurrence of the pattern in the input string
    match = re.search(pattern, input_string)
    
    # If match is found, return the string within parentheses
    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":
    main_dl()
    unreviewed_row_indices = find_unreviewed_indices("RawForm.csv", "ReviewedForm.csv")
    print("There are", len(unreviewed_row_indices), "new rows.")
    for row_number in find_unreviewed_indices("RawForm.csv", "ReviewedForm.csv"):
        edit_csv("RawForm.csv", "ReviewedForm.csv", row_number, connection)
    csv_to_sql("ReviewedForm.csv")