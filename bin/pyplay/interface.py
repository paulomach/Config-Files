# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from debtutils import DebtUtils

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(550, 300)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 530, 221))
        font = QtGui.QFont()
        font.setFamily("Droid Sans Mono")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 250, 175, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.updateData)
        self.pushButton_2.clicked.connect(lambda: self.saveData(self.plainTextEdit.toPlainText()))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Dialog", "Get Data"))
        self.pushButton_2.setText(_translate("Dialog", "Open sheet"))

    def updateData(self):
        self.plainTextEdit.clear()
        info = DebtUtils.dataRetrieve().replace('.', ',')
        self.plainTextEdit.appendPlainText(info)

    def saveData(self,  inputData):
        DebtUtils.saveContent(inputData)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

