import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']
SHARED_DRIVE_ID = '0AGsI-FsgSjnKUk9PVA'

def get_folder_list():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    folders = []
    page_token = None
    
    while True:
        results = service.files().list(
            q=f"mimeType='application/vnd.google-apps.folder' and '{SHARED_DRIVE_ID}' in parents",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            driveId=SHARED_DRIVE_ID,
            corpora='drive',
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
            pageSize=1000
        ).execute()

        folders.extend(results.get('files', []))
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

    return folders

folder_list = get_folder_list()

print(f"Total folders found: {len(folder_list)}")
for folder in folder_list:
    print(f"Folder Name: {folder['name']}, Folder ID: {folder['id']}")