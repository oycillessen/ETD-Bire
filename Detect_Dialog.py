# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Detect_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Detect_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(328, 174)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 140, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 60, 21))
        self.label.setObjectName("label")
        self.Listen_card = QtWidgets.QComboBox(Dialog)
        self.Listen_card.setGeometry(QtCore.QRect(70, 20, 81, 21))
        self.Listen_card.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.Listen_card.setObjectName("Listen_card")
        self.Listen_card.addItem("")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(67, 50, 251, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AP_list = QtWidgets.QLabel(self.layoutWidget)
        self.AP_list.setEnabled(True)
        self.AP_list.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.AP_list.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_list.setObjectName("AP_list")
        self.verticalLayout.addWidget(self.AP_list)
        self.AP_akm = QtWidgets.QLabel(self.layoutWidget)
        self.AP_akm.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_akm.setObjectName("AP_akm")
        self.verticalLayout.addWidget(self.AP_akm)
        self.AP_key = QtWidgets.QLineEdit(self.layoutWidget)
        self.AP_key.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.AP_key.setAlignment(QtCore.Qt.AlignCenter)
        self.AP_key.setObjectName("AP_key")
        self.verticalLayout.addWidget(self.AP_key)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 50, 60, 71))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_5 = QtWidgets.QLabel(self.splitter)
        self.label_5.setObjectName("label_5")
        self.label_9 = QtWidgets.QLabel(self.splitter)
        self.label_9.setObjectName("label_9")
        self.label_4 = QtWidgets.QLabel(self.splitter)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(169, 20, 61, 21))
        self.label_2.setObjectName("label_2")
        self.Send_card = QtWidgets.QComboBox(Dialog)
        self.Send_card.setGeometry(QtCore.QRect(230, 20, 91, 21))
        self.Send_card.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.Send_card.setObjectName("Send_card")
        self.Send_card.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Detect Option"))
        self.label.setText(_translate("Dialog", "Monitor："))
        self.AP_key.setPlaceholderText(_translate("Dialog", "Enter Password"))
        self.AP_key.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_5.setText(_translate("Dialog", "Number："))
        self.label_9.setText(_translate("Dialog", "ENC-AUTH："))
        self.label_4.setText(_translate("Dialog", "Password："))
        self.label_2.setText(_translate("Dialog", "Sender："))
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

    def get_listen_card(self):

        return self.Listen_card.currentText()

    def get_send_card(self):

        return self.Send_card.currentText()

    def get_ap_key(self):

        return self.AP_key.text()

