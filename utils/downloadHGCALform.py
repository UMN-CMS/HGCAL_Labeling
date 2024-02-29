import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of your specific spreadsheet.
SPREADSHEET_ID = "1Y_fhllebp5jrWqHVwADHX0AIzJudbHyHFT-iDteq8ow"
RANGE_NAME = "Form Responses 1!A1:Z"

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

def main():
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
        download_csv(service, SPREADSHEET_ID, RANGE_NAME, "HGCAL_Labeling_Request_Form.csv")

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
