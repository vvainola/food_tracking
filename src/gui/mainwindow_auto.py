# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btn_scan = QtWidgets.QPushButton(self.centralWidget)
        self.btn_scan.setGeometry(QtCore.QRect(0, 0, 91, 51))
        self.btn_scan.setObjectName("btn_scan")
        self.table_eaten_today = QtWidgets.QTableWidget(self.centralWidget)
        self.table_eaten_today.setGeometry(QtCore.QRect(100, 0, 691, 401))
        self.table_eaten_today.setObjectName("table_eaten_today")
        self.table_eaten_today.setColumnCount(8)
        self.table_eaten_today.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_eaten_today.setHorizontalHeaderItem(7, item)
        self.table_eaten_today.horizontalHeader().setDefaultSectionSize(85)
        self.table_eaten_today.horizontalHeader().setStretchLastSection(True)
        self.btn_search = QtWidgets.QPushButton(self.centralWidget)
        self.btn_search.setGeometry(QtCore.QRect(0, 60, 91, 51))
        self.btn_search.setObjectName("btn_search")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 42))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Food tracker"))
        self.btn_scan.setText(_translate("MainWindow", "Scan"))
        item = self.table_eaten_today.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Code"))
        item = self.table_eaten_today.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.table_eaten_today.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Amount"))
        item = self.table_eaten_today.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Cals"))
        item = self.table_eaten_today.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Prot"))
        item = self.table_eaten_today.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Carbs (sug)"))
        item = self.table_eaten_today.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Fat (sat)"))
        item = self.table_eaten_today.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Salt"))
        self.btn_search.setText(_translate("MainWindow", "Search"))
