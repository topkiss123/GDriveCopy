# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(650, 471)
        MainWindow.setWindowFilePath("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.credentials_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.credentials_label.sizePolicy().hasHeightForWidth())
        self.credentials_label.setSizePolicy(sizePolicy)
        self.credentials_label.setObjectName("credentials_label")
        self.horizontalLayout.addWidget(self.credentials_label)
        self.cred_status_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cred_status_label.sizePolicy().hasHeightForWidth())
        self.cred_status_label.setSizePolicy(sizePolicy)
        self.cred_status_label.setObjectName("cred_status_label")
        self.horizontalLayout.addWidget(self.cred_status_label)
        self.file_browser = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_browser.sizePolicy().hasHeightForWidth())
        self.file_browser.setSizePolicy(sizePolicy)
        self.file_browser.setObjectName("file_browser")
        self.horizontalLayout.addWidget(self.file_browser)
        self.change_cred = QtWidgets.QPushButton(self.centralwidget)
        self.change_cred.setObjectName("change_cred")
        self.horizontalLayout.addWidget(self.change_cred)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.folder_label = QtWidgets.QLabel(self.centralwidget)
        self.folder_label.setObjectName("folder_label")
        self.horizontalLayout_2.addWidget(self.folder_label)
        self.folder_id = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folder_id.sizePolicy().hasHeightForWidth())
        self.folder_id.setSizePolicy(sizePolicy)
        self.folder_id.setMaximumSize(QtCore.QSize(16777215, 25))
        self.folder_id.setAcceptDrops(False)
        self.folder_id.setObjectName("folder_id")
        self.horizontalLayout_2.addWidget(self.folder_id)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.authorize = QtWidgets.QPushButton(self.centralwidget)
        self.authorize.setObjectName("authorize")
        self.horizontalLayout_3.addWidget(self.authorize)
        self.copy = QtWidgets.QPushButton(self.centralwidget)
        self.copy.setObjectName("copy")
        self.horizontalLayout_3.addWidget(self.copy)
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setObjectName("clear")
        self.horizontalLayout_3.addWidget(self.clear)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.authorize.clicked.connect(MainWindow.authorize_clicked)
        self.copy.clicked.connect(MainWindow.copy_clicked)
        self.clear.clicked.connect(MainWindow.clear_clicked)
        self.file_browser.clicked.connect(MainWindow.browser_clicked)
        self.change_cred.clicked.connect(MainWindow.change_cred)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GDriveCopy"))
        self.credentials_label.setText(_translate("MainWindow", "Credentials :"))
        self.cred_status_label.setText(_translate("MainWindow", "None."))
        self.file_browser.setText(_translate("MainWindow", "Import"))
        self.change_cred.setText(_translate("MainWindow", "Delete Credentials"))
        self.folder_label.setText(_translate("MainWindow", "Folder ID :"))
        self.authorize.setText(_translate("MainWindow", "Authorize"))
        self.copy.setText(_translate("MainWindow", "Start Copy"))
        self.clear.setText(_translate("MainWindow", "Clear Log"))

