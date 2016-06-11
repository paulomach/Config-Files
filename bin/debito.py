# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debts.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from lxml import html
import requests

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 500, 231))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.raise_()
        self.pushButton.clicked.connect(self.dataRetrieve)
        self.plainTextEdit.raise_()
        self.plainTextEdit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Retrieve Data"))
    
    def dataRetrieve(self):
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText("retrieving data from source...")
        # http://www.sidra.ibge.gov.br/AjudaAPISidra.htm
        # http://www.sidra.ibge.gov.br/bda/tabela/protabl.asp?c=1737&z=ia&o=3&i=P
        # http://www.sidra.ibge.gov.br/api/values/t/1737/p/201509-201605/v/63/n1/1/h/n/f/c
        url = "http://www.ibge.gov.br/home/estatistica/indicadores/precos/inpc_ipca/ipca-inpc_201604_1.shtm"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table[@summary="Tabela com série histórica IPCA"]/thead/tr/td')
        j = 0
        k = 0
        ipca = [];
        for i in table:
            value = i.text_content().strip()
            if j == 1:
                if value == "Set":
                    j = 2
            if j == 2:
                if value.isalpha():
                    k = 0
                k += 1
                if k == 3:
                    ipca.append(float(value.replace(',','.')))
            if value == "2015":
                j = 1
        #        9,  10,11,12   1,2,3,4
        drawee = [70000,0,0,10000,0,0,0,31500,31500]
        dates = ["21/09/2015", "21/12/2015", "20/04/2016","20/05/2016"]
        k = 0
        leftover = 0
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(
            "Data;Retirada;IPCA acumulado;Corrigido;Saldo")
        for i in range(0,len(drawee)):
            if drawee[i] > 0:
                interest = 1
                for j in range(i,len(ipca)-1):
                    interest = interest*(1+ipca[j]/100)
                accumulated = round((interest-1), 4)
                corrected = round(drawee[i]*interest, 2)
                leftover = round(corrected + leftover, 2)
                text = dates[k] + ";" + str(drawee[i]) + ";" + str(accumulated).replace('.', ',')\
                + ";" + str(corrected).replace('.', ',') + ";" + str(leftover).replace('.', ',')
                self.plainTextEdit.appendPlainText(text)
                k += 1



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

