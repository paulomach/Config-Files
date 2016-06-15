#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from debtutils import DebtUtils
from datetime import datetime

class Ui_Dialog(object):
    ipca=[]
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Debt calculation")
        Dialog.setFixedSize(550, 300)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 530, 221))
        font = QtGui.QFont()
        font.setFamily("Droid Sans Mono")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 250, 300, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.buttonGet = QtWidgets.QPushButton(self.splitter)
        self.buttonGet.setObjectName("buttonGet")
        self.buttonOpen = QtWidgets.QPushButton(self.splitter)
        self.buttonOpen.setObjectName("buttonOpen")
        self.buttonIpca = QtWidgets.QPushButton(self.splitter)
        self.buttonIpca.setObjectName("buttonIpca")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.buttonGet.clicked.connect(self.updateData)
        self.buttonOpen.clicked.connect(lambda: self.saveData(self.plainTextEdit.toPlainText()))
        self.buttonIpca.clicked.connect(self.printIpca)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.buttonGet.setText(_translate("Dialog", "Get Data"))
        self.buttonOpen.setText(_translate("Dialog", "Open sheet"))
        self.buttonIpca.setText(_translate("Dialog",  "IPCA print"))
        self.buttonIpca.setEnabled(False);
        self.buttonOpen.setEnabled(False);

    def updateData(self):
        if len(self.ipca) > 0:
            info = self.plainTextEdit.toPlainText()
        else:
            info,  self.ipca = DebtUtils.dataRetrieve()
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(info.replace('.', ','))
        if info == "":
            self.buttonIpca.setEnabled(False);
            self.buttonOpen.setEnabled(False);
        else:
            self.buttonIpca.setEnabled(True);
            self.buttonOpen.setEnabled(True);

    def saveData(self,  inputData):
        DebtUtils.saveContent(inputData)
    
    def printIpca(self):
        self.plainTextEdit.appendPlainText("Mês;IPCA")
        for i in self.ipca:
            info =  datetime.strptime(i.get('D1C'),"%Y%m").strftime("%b/%Y")  + ";" + str(round(float(i.get('V'))/100, 4)).replace('.',',')
            self.plainTextEdit.appendPlainText(info)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

