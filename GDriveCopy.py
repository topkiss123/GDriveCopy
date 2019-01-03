from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
from mainwindow import Ui_MainWindow
from enum import Enum, unique, auto
import time
import json
import sys
import os
import configparser

SCOPES = 'https://www.googleapis.com/auth/drive'


def authorize(credentials, log_callback=None):
    if log_callback:
        log_callback('Start to check authorize...')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        try:
            flow = client.flow_from_clientsecrets(credentials, SCOPES)
            creds = tools.run_flow(flow, store)
        except:
            if log_callback:
                log_callback('Authorize Fail...')
    if creds:
        service = build('drive', 'v3', http=creds.authorize(Http()))
        if service:
            if log_callback:
                log_callback('Authorize Success...')
            return service

    return None


def start_copy(service, folder_id, log_callback=None):
    if log_callback:
        log_callback('Start to Copy...')
    clone_folder_files = get_files(service=service, folder_id=folder_id, log_callback=log_callback)
    if log_callback:
        log_callback('Need to Clone Files:')
    for item in clone_folder_files:
        if log_callback:
            log_callback(u'{0} ({1})'.format(item['name'], item['id']))

    clone_folder_name = get_folder_name(service=service, folder_id=folder_id, log_callback=log_callback)
    folder_id = get_user_folder(service=service, folder_name=clone_folder_name, log_callback=log_callback)
    copy_files(service=service, to_folder=folder_id, files=clone_folder_files, log_callback=log_callback)
    if log_callback:
        log_callback('Copy done...')


def create_folder(service, name, log_callback=None):
    if log_callback:
        log_callback('Create folder...')
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    response = service.files().create(body=file_metadata, fields='id').execute()
    if log_callback:
        log_callback('Create folder...Done. Folder ID: {0}'.format(response.get('id', None)))
    return response.get('id', None)


def get_files(service, folder_id, log_callback=None):
    if log_callback:
        log_callback('Get files...')
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
        if log_callback:
            log_callback('Get files...Done. No files found.')
    else:
        if log_callback:
            log_callback('Get files...Done.')

    return items


def get_folder_name(service, folder_id, log_callback=None):
    if log_callback:
        log_callback('Get folder name...')
    response = service.files().get(fileId=folder_id).execute()
    if 'name' in response:
        folder_name = response['name'] + '_byGDriveCopy'
        if log_callback:
            log_callback('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name
    else:
        folder_name = 'Copy_byGDriveCopy' + time.strftime("%Y-%m-%d", time.localtime())
        if log_callback:
            log_callback('Get folder name...Done. Name: {0}'.format(folder_name))
        return folder_name


def get_user_folder(service, folder_name, log_callback=None):
    if log_callback:
        log_callback('Get user folder...')
    query_name = '"' + folder_name + '"'
    query = "name=" + query_name + "and trashed=false"
    response = service.files().list(orderBy='folder', q=query, fields="files(id, name)").execute()
    result = response.get('files', [])
    if not result:
        if log_callback:
            log_callback('Get user folder...Done.')
        return create_folder(service=service, name=folder_name, log_callback=log_callback)
    else:
        if 'id' in result[0]:
            if log_callback:
                log_callback('Get user folder...Done.')
            return result[0]['id']
        else:
            if log_callback:
                log_callback('Get user folder...Done.')
            return create_folder(service=service, name=folder_name, log_callback=log_callback)


def copy_files(service, to_folder, files, log_callback=None):
    if log_callback:
        log_callback('Copy Files...')
    user_folder_files = get_files(service=service, folder_id=to_folder, log_callback= log_callback)

    if log_callback:
        log_callback('User Files:')
    for item in user_folder_files:
        if log_callback:
            log_callback(u'{0} ({1})'.format(item['name'], item['id']))

    for file in files:
        if not check_file(user_files=user_folder_files, copy_file=file, log_callback=log_callback):
            file_name = file['name']
            file_id = file['id']
            file_metadata = {
                'name': file_name,
                'parents': [to_folder]
            }

            try:
                time.sleep(0.5)
                service.files().copy(fileId=file_id, body=file_metadata).execute()
                if log_callback:
                    log_callback('Copy Files...Copy: {0}'.format(file_name))
            except HttpError as err:
                content = json.loads(err.content)
                if log_callback:
                    log_callback('Unexpected error: {0}'.format(content))
                break
    if log_callback:
        log_callback('Copy Files...Done.')


def check_file(user_files, copy_file, log_callback=None):
    result = False
    for file in user_files:
        if file['name'] == copy_file['name']:
            if log_callback:
                log_callback('Checking file...{0} is exist'.format(file['name']))
            result = True
    return result


@unique
class ActionType(Enum):
    Authorize = auto()
    Copy = auto()


class WorkThread(QtCore.QThread):

    authorize_signal = QtCore.pyqtSignal(object)
    log_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(WorkThread, self).__init__()
        self.service = None
        self.folder_id = None
        self.credentials = None
        self.action_type = None

    def __del__(self):
        self.wait()

    def authorize(self, credentials):
        self.action_type = ActionType.Authorize
        self.credentials = credentials
        self.start()

    def start_copy(self, service, folder_id):
        self.action_type = ActionType.Copy
        self.service = service
        self.folder_id = folder_id
        self.start()

    def run(self):
        if self.action_type == ActionType.Authorize:
            drive_service = authorize(credentials=self.credentials, log_callback=self.callback)
            self.authorize_signal.emit(drive_service)
        elif self.action_type == ActionType.Copy:
            if self.service:
                if self.folder_id:
                    start_copy(service=self.service, folder_id=self.folder_id, log_callback=self.callback)
                else:
                    self.callback('NOTICE: Folder Id is empty...')

    def callback(self, log_string):
        self.log_signal.emit(log_string)


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.work_thread = WorkThread()
        self.work_thread.log_signal.connect(self.log_callback)
        self.work_thread.authorize_signal.connect(self.authorize_callback)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        self.main_window.copy.setEnabled(False)
        self.main_window.authorize.setEnabled(False)
        self.drive_service = None
        self.credentials = None
        self._file_path = None
        self.saved_folder = None
        self.config = configparser.ConfigParser()
        self.restore_value()
        self.show()

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        if path:
            self._file_path = path
            self.set_path_config(self._file_path)
            self.main_window.credentials_path.setPlainText(self._file_path)
            _, self.credentials = os.path.split(self._file_path)
            if self.credentials:
                self.main_window.authorize.setEnabled(True)
            else:
                self.main_window.authorize.setEnabled(False)

    def set_path_config(self, path):
        if 'SETTING' not in self.config:
            self.config['SETTING'] = {}
        self.config['SETTING']['Path'] = path
        with open('GDriveCopy.ini', 'w') as configfile:
            self.config.write(configfile)

    def set_folder_config(self, folder):
        if 'SETTING' not in self.config:
            self.config['SETTING'] = {}
        self.config['SETTING']['Folder'] = folder
        with open('GDriveCopy.ini', 'w') as configfile:
            self.config.write(configfile)

    def restore_value(self):
        self.config.read('GDriveCopy.ini')
        if 'SETTING' in self.config:
            self.file_path = self.config['SETTING']['Path']
            if 'Folder' in self.config['SETTING']:
                self.main_window.folder_id.setPlainText(self.config['SETTING']['Folder'])

    def log_callback(self, log_string):
        print(log_string)
        self.main_window.textBrowser.append(log_string)

    def authorize_callback(self, service):
        self.drive_service = service
        if self.drive_service:
            self.main_window.copy.setEnabled(True)
        else:
            self.main_window.copy.setEnabled(False)

    @pyqtSlot()
    def authorize_clicked(self):
        self.work_thread.authorize(self.credentials)

    @pyqtSlot()
    def copy_clicked(self):
        clone_folder = self.main_window.folder_id.toPlainText()
        self.set_folder_config(clone_folder)
        self.work_thread.start_copy(self.drive_service, clone_folder)

    @pyqtSlot()
    def clear_clicked(self):
        self.main_window.textBrowser.setPlainText('')

    @pyqtSlot()
    def browser_clicked(self):
        dialog = QFileDialog()
        options = dialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(dialog, '', '', 'JSON (*.json)', options=options)
        # if file_path:
        #     self.main_window.credentials_path.setPlainText(file_path)
        #     _, self.credentials = os.path.split(file_path)
        #     if self.credentials:
        #         self.main_window.authorize.setEnabled(True)
        #     else:
        #         self.main_window.authorize.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())