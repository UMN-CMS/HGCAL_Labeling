#FormToSQL README
##Instructions
1. Getting started
   First you must create the credentials.json file containing the client id and necessary
   passcodes, as well as configure your google OAuth.

   Follow the "Set up your environment" quick start guide below using a gmail account
   with access to the google forms output in sheets: Enable the API, Configure the OAuth consent screen,
   Authorize credentials for a desktop application, Install the Google client library.

   [Google API Quickstart Guide](https://developers.google.com/sheets/api/quickstart/python)

   The pulldown of the google sheets is largely based on the quickstart.py example code.
   At the bottom of the code in the executable section, update the SCOPES and 
   SPREADSHEET_ID variables to that of the spreadsheet in use. 

   Next, download all libraries within the requirements.txt file.
   This can be done using pip:
   'pip install -r requirements.txt'

   Before continuing, be sure that the MySQL server is setup. Fill in the "connection" function 
   with the details of the MySQL server.

   Once set up correctly, the raw data from the Google forms will be downloaded
   in CSV format to a file titled "RawForm.csv"
   
2. Using the code
   The code can be run with 'python3 FormToSQL' in the appropriate directory.

   After pulling down the Form data, the program will check for new entries. If the
   entry is new, it will print the contents of the form into the terminal for manual review.
   If everything looks correct, enter "y" or press enter in the terminal to move onto the next
   entry. 
   
   If something looks off, enter "N" into the terminal. This will allow you to cycle through
   rows of the entry one by one, entering "N" to edit and "y" to skip each row.

   The program will then check if the major type and sub types are valid and compatible.
   If not, the program will again ask for user input until a valid combination is input.

   Once this is complete the corrector's job is done. the corrected inputs will then be saved 
   as ReviewedForm.csv. The data being saved into the MySQL server is then put into the correct 
   format, saved as a filtered csv file, and then finally each row will be pushed into the MySQL 
   server ONLY IF IT IS UNIQUE.
   
   Copying and pasting of form input can lead to duplicate rows that will not be pushed properly,
   be sure to at least change the time of the order to prevent this issue.

   If a mistake is made when reviewing a row, edit the row manuelly in the csv file instead
   of exiting the script prematurely, as this can cause issues that will crash the code later
   on. Always let the script finish before exiting or editing an entry to prevent a crash that
   may lead to having to reset the ReviewedForm.csv. In the event this occures, delete all csv
   files and run the code again. This will require the manuel rentery of all mistakes already
   fixed, but will fix the code, so please avoid this by not exiting the code until it is finished.



3. Adding a new columns
   To add a new column of data to be saved to the SQL database, first this new column must be added
   to the MySQL server. Secondly, in the csv_to_sql function in FormToSQL.py code add the column name
   to the list needed_columns. Then add it to the dictionary titled column_mapping in the order of
   appearence in the SQL database. Here, the key will be SQL column name while the value will be the 
   csv column name. 

   Next, add the csv column name to the columns list in the find_unreviewed_indices function. Lastly,
   if you want the new column to be considered in the check for duplicate rows, add the new column
   accodingly in the bottom of csv_to_sql section commented "if new, uploads to mysql".
