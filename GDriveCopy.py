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
    drive_service = authorize(credentials='credentials.json')
    clone_folder = '14JXKLEVq4cHOCuNsBnZGKEOrp8DvIba8'
    start_copy(service=drive_service, folder_id=clone_folder)


def authorize(credentials):
    print('Start to check authorize...')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def start_copy(service, folder_id):
    print('Start to Copy...')
    clone_folder = '14JXKLEVq4cHOCuNsBnZGKEOrp8DvIba8'
    clone_folder_files = get_files(service=service, folder_id=folder_id)

    print('Need to Clone Files:')
    for item in clone_folder_files:
        print(u'{0} ({1})'.format(item['name'], item['id']))

    clone_folder_name = get_folder_name(service=service, folder_id=clone_folder)
    folder_id = get_user_folder(service=service, folder_name=clone_folder_name)
    copy_files(service=service, to_folder=folder_id, files=clone_folder_files)
    print('Copy done...')


def create_folder(service, name):
    print('Create folder...')
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    response = service.files().create(body=file_metadata, fields='id').execute()
    print('Create folder...Done. Folder ID: {0}'.format(response.get('id', None)))
    return response.get('id', None)


def get_files(service, folder_id):
    print('Get files...')
    query = "'" + folder_id + "' in parents"

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
        print('Get files...Done. No files found.')
    else:
        print('Get files...Done.')

    return items


def get_folder_name(service, folder_id):
    print('Get folder name...')
    response = service.files().get(fileId=folder_id).execute()
    if 'name' in response:
        folder_name = response['name'] + '_byGDriveCopy'
        print('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name
    else:
        folder_name = 'Copy_byGDriveCopy' + time.strftime("%Y-%m-%d", time.localtime())
        print('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name


def get_user_folder(service, folder_name):
    print('Get user folder...')
    query = "name='" + folder_name + "'and trashed=false"
    response = service.files().list(orderBy='folder', q=query, fields="files(id, name)").execute()
    result = response.get('files', [])
    if not result:
        print('Get user folder...Done.')
        return create_folder(service=service, name=folder_name)
    else:
        if 'id' in result[0]:
            print('Get user folder...Done.')
            return result[0]['id']
        else:
            print('Get user folder...Done.')
            return create_folder(service=service, name=folder_name)


def copy_files(service, to_folder, files):
    print('Copy Files...')
    user_folder_files = get_files(service=service, folder_id=to_folder)

    print('User Files:')
    for item in user_folder_files:
        print(u'{0} ({1})'.format(item['name'], item['id']))

    for file in files:
        if not check_file(user_files=user_folder_files, copy_file=file):
            file_name = file['name']
            file_id = file['id']
            file_metadata = {
                'name': file_name,
                'parents': [to_folder]
            }

            try:
                time.sleep(1)
                service.files().copy(fileId=file_id, body=file_metadata).execute()
                print('Copy Files...Copy: {0}'.format(file_name))
            except HttpError as err:
                content = json.loads(err.content)
                print('Unexpected error: {0}'.format(content))
                break
    print('Copy Files...Done.')


def check_file(user_files, copy_file):
    result = False
    for file in user_files:
        if file['name'] == copy_file['name']:
            print('Checking file...{0} is exist'.format(file['name']))
            result = True
    return result


if __name__ == '__main__':
    main()
