import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Replace these values with your own
credentials_file = 'path/to/credentials.json'
spreadsheet_name = 'Your Spreadsheet Name'
worksheet_name = 'Sheet1'  # Change to the name of your sheet
local_excel_file = 'path/to/local_excel_file.xlsx'
folder_id = 'your_google_drive_folder_id'

# Authenticate with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet = gc.open(spreadsheet_name)

# Open the worksheet
worksheet = spreadsheet.worksheet(worksheet_name)

# Upload the local Excel file to Google Drive folder
drive_folder = gc.create('TemporaryFolder', folder_id=folder_id)
file_in_drive = gc.import_excel(drive_folder['id'], local_excel_file)

print(f"File uploaded to Google Drive folder: {file_in_drive['title']}")
