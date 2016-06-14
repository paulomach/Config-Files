# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debts.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from collections import OrderedDict
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
        self.plainTextEdit.setReadOnly(1)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Debt Calc"))
        self.pushButton.setText(_translate("MainWindow", "Retrieve Data"))
    
    def dataRetrieve(self):
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText("retrieving data from source...")
        url = "http://www.sidra.ibge.gov.br/api/values/t/1737/p/201509-201704/v/63/n1/1/h/n/f/c"
        ipca = requests.get(url).json()
        # script updatable 
        drawee = {'201509':70000, '201512':10000, '201604':31500, '201605':31500}
        drawee = OrderedDict(sorted(drawee.items()))
        
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(
            "Data;Retirada;Indice acumulado;Valor Corrigido;Saldo Atualizado")
        
        vtotal=0
        for d, v in drawee.items():
            index = 1
            for i in range(0, len(ipca)):
                if ipca[i].get('D1C') == d:
                    break
            for j in range(i, len(ipca)):
                index = index*(1+ float(ipca[j].get('V'))/100)
            vtotal = round(vtotal+v*index, 2)
            line = datetime.strptime(d,"%Y%m").strftime("%b/%Y") + ";" + str(v) + ";" +\
            str(index-1) + ";" + str(round(v*index, 2)) + ";" + str(vtotal)
            self.plainTextEdit.appendPlainText(line.replace(".", ","))
        
        self.saveContent()
    
    def saveContent(self):
        filename = "teste.csv"
        fd = open(filename, 'w')
        fd.write(self.plainTextEdit.toPlainText())
        fd.flush()
        fd.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
