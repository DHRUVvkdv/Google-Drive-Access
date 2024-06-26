import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SHARED_DRIVE_ID = '0AGsI-FsgSjnKUk9PVA'
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_folder_list():
    creds = get_credentials()
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

def main():
    folder_list = get_folder_list()
    print(f"Total folders found: {len(folder_list)}")
    for folder in folder_list:
        print(f"Folder Name: {folder['name']}, Folder ID: {folder['id']}")

if __name__ == '__main__':
    main()