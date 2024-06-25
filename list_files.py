from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'service-account-file.json'

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('drive', 'v3', credentials=credentials)

# Shared drive ID
SHARED_DRIVE_ID = 'your-shared-drive-id'

# List files in shared drive
results = service.files().list(
    pageSize=10,
    fields="nextPageToken, files(id, name)",
    supportsAllDrives=True,
    includeItemsFromAllDrives=True,
    driveId=SHARED_DRIVE_ID,
    corpora='drive'
).execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f'{item["name"]} ({item["id"]})')
