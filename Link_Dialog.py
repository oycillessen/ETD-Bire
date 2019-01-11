# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Link_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Link_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(237, 174)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 140, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(21, 11, 203, 112))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.interface_choose = QtWidgets.QComboBox(self.widget)
        self.interface_choose.setObjectName("comboBox_2")
        self.horizontalLayout.addWidget(self.interface_choose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.AP_ssid = QtWidgets.QLabel(self.widget)
        self.AP_ssid.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_ssid.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.AP_ssid)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.AP_akm = QtWidgets.QLabel(self.widget)
        self.AP_akm.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_akm.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.AP_akm)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.AP_bssid = QtWidgets.QLabel(self.widget)
        self.AP_bssid.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_bssid.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.AP_bssid)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.AP_key = QtWidgets.QLineEdit(self.widget)
        self.AP_key.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_key.setObjectName("lineEdit")
        self.horizontalLayout_5.addWidget(self.AP_key)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Connect Option"))
        self.label.setText(_translate("Dialog", "Interface："))
        self.label_2.setText(_translate("Dialog", "SSID："))
        self.label_9.setText(_translate("Dialog", "ENC-AUTH："))
        self.label_3.setText(_translate("Dialog", "BSSID："))
        self.label_4.setText(_translate("Dialog", "Password："))
        self.AP_key.setPlaceholderText(_translate("Dialog", "Enter Password"))
        self.AP_key.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

    def get_interface(self):

        interface = self.interface_choose.currentText()
        return interface

    def get_AP_Key(self):

        key = self.AP_key.text()
        return key
