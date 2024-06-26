import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SHARED_DRIVE_ID = '0AGsI-FsgSjnKUk9PVA'
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

# Define all possible Google Workspace document types
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

def main(file_type):
    files = list_files(file_type)
    total_size = sum(int(file.get('size', 0)) for file in files)

    output_file = f'file_list_{file_type}.txt'
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(f"Total {file_type.upper()} files found: {len(files)}\n")
        output.write(f"Total size of {file_type.upper()} files: {total_size / (1024*1024):.2f} MB\n\n")
        output.write(f"List of {file_type.upper()} files:\n")

        for file in files:
            size = int(file.get('size', 0)) / (1024*1024)
            output.write(f"Name: {file['name']}\n")
            output.write(f"Size: {size:.2f} MB\n")
            output.write(f"ID: {file['id']}\n")
            output.write("--------------------\n")

    print(f"Output has been saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List files of a specific type in a shared drive.')
    parser.add_argument('file_type', choices=FILE_TYPES.keys(), help='Type of files to list')
    args = parser.parse_args()

    main(args.file_type)