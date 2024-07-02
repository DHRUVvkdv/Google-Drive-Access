import os
import json
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SHARED_DRIVE_ID = '0AGsI-FsgSjnKUk9PVA'
TOKEN_FILE = '../secret/token.json'
CREDENTIALS_FILE = '../secret/credentials.json'

FILE_TYPES = {
    'document': 'application/vnd.google-apps.document',
    'spreadsheet': 'application/vnd.google-apps.spreadsheet',
    'presentation': 'application/vnd.google-apps.presentation',
    'drawing': 'application/vnd.google-apps.drawing',
    'form': 'application/vnd.google-apps.form',
    'script': 'application/vnd.google-apps.script',
    'site': 'application/vnd.google-apps.site',
    'pdf': 'application/pdf',
    'folder': 'application/vnd.google-apps.folder'
}

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

def list_files(file_type):
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    mime_type = FILE_TYPES[file_type]
    query = f"mimeType='{mime_type}'"

    files = []
    page_token = None
    
    while True:
        try:
            results = service.files().list(
                q=query,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                driveId=SHARED_DRIVE_ID,
                corpora='drive',
                fields="nextPageToken, files(id, name, size)",
                pageToken=page_token,
                pageSize=1000
            ).execute()

            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return files

def fetch_and_store(file_type):
    files = list_files(file_type)
    total_size = sum(int(file.get('size', 0)) for file in files)

    output_data = {
        "file_type": file_type,
        "total_files": len(files),
        "total_size_mb": round(total_size / (1024*1024), 2),
        "files": []
    }

    for file in files:
        size = int(file.get('size', 0)) / (1024*1024)
        output_data["files"].append({
            "name": file['name'],
            "id": file['id'],
            "size_mb": round(size, 2)
        })

    output_file = f'../data/json/file_list_{file_type}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Data for {file_type} has been saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch and store Google Drive file data.')
    parser.add_argument('file_type', choices=FILE_TYPES.keys(), help='Type of files to fetch')
    args = parser.parse_args()

    fetch_and_store(args.file_type)