from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
import time
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    print('Start to check authorize...')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    print('Start to Copy...')
    # Call the Drive v3 API
    clone_folder = '14JXKLEVq4cHOCuNsBnZGKEOrp8DvIba8'
    clone_folder_files = get_clone_files(service=drive_service, floder_id=clone_folder)
    clone_folder_name = get_folder_name(service=drive_service, floder_id=clone_folder)
    folder_id = create_folder(service=drive_service, name=clone_folder_name)
    copy_files(service=drive_service, to_folder=folder_id, files=clone_folder_files)
    print('Copy done...')


def create_folder(service, name):
    # Can check folder first, make function better
    print('Create folder...')
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    response = service.files().create(body=file_metadata, fields='id').execute()
    print('Create folder...Done. Folder ID: {0}'.format(response.get('id', None)))
    return response.get('id', None)


def get_clone_files(service, floder_id):
    print('Get clone files...')
    query = "'" + floder_id + "' in parents"

    items = []
    next_page_token = None

    while True:
        response = service.files().list(q=query, orderBy='name', pageSize=1000, pageToken=next_page_token,
                                       fields="nextPageToken, files(id, name)").execute()
        items += response.get('files', [])
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

    if not items:
        print('Get clone files...Done. No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
        print('Get clone files...Done.')

    return items


def get_folder_name(service, floder_id):
    print('Get folder name...')
    response = service.files().get(fileId=floder_id).execute()
    if 'name' in response:
        folder_name = response['name'] + '_byGDriveCopy'
        print('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name
    else:
        folder_name = 'Copy_byGDriveCopy' + time.strftime("%Y-%m-%d", time.localtime())
        print('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name


def copy_files(service, to_folder, files):
    print('Copy Files...')
    for file in files:
        file_name = file['name']
        file_id = file['id']
        file_metadata = {
            'name': file_name,
            'parents': [to_folder]
        }

        try:
            service.files().copy(fileId=file_id, body=file_metadata).execute()
            print('Copy Files...Copy: {0}'.format(file_name))
        except HttpError as err:
            content = json.loads(err.content)
            print('Unexpected error: {0}'.format(content))
            break
    print('Copy Files...Done.')


if __name__ == '__main__':
    main()
