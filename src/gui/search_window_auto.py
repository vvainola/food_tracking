# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_search_form(object):
    def setupUi(self, search_form):
        search_form.setObjectName("search_form")
        search_form.resize(776, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(search_form.sizePolicy().hasHeightForWidth())
        search_form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        search_form.setFont(font)
        self.centralwidget = QtWidgets.QWidget(search_form)
        self.centralwidget.setObjectName("centralwidget")
        self.table_search = QtWidgets.QTableWidget(self.centralwidget)
        self.table_search.setGeometry(QtCore.QRect(0, 50, 771, 181))
        self.table_search.setObjectName("table_search")
        self.table_search.setColumnCount(9)
        self.table_search.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_search.setHorizontalHeaderItem(8, item)
        self.table_search.horizontalHeader().setDefaultSectionSize(85)
        self.box_search = QtWidgets.QLineEdit(self.centralwidget)
        self.box_search.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.box_search.setText("")
        self.box_search.setObjectName("box_search")
        self.btn_name = QtWidgets.QRadioButton(self.centralwidget)
        self.btn_name.setGeometry(QtCore.QRect(220, 10, 121, 31))
        self.btn_name.setObjectName("btn_name")
        self.bnt_barcode = QtWidgets.QRadioButton(self.centralwidget)
        self.bnt_barcode.setGeometry(QtCore.QRect(300, 10, 151, 31))
        self.bnt_barcode.setObjectName("bnt_barcode")
        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(QtCore.QRect(400, 10, 81, 31))
        self.btn_quit.setObjectName("btn_quit")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(710, 10, 51, 31))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(640, 10, 71, 31))
        self.btn_save.setObjectName("btn_save")
        self.btn_new = QtWidgets.QPushButton(self.centralwidget)
        self.btn_new.setGeometry(QtCore.QRect(480, 10, 61, 31))
        self.btn_new.setObjectName("btn_new")
        self.btn_remove = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remove.setGeometry(QtCore.QRect(540, 10, 101, 31))
        self.btn_remove.setObjectName("btn_remove")
        search_form.setCentralWidget(self.centralwidget)

        self.retranslateUi(search_form)
        QtCore.QMetaObject.connectSlotsByName(search_form)

    def retranslateUi(self, search_form):
        _translate = QtCore.QCoreApplication.translate
        search_form.setWindowTitle(_translate("search_form", "Search"))
        item = self.table_search.horizontalHeaderItem(0)
        item.setText(_translate("search_form", "Barcode"))
        item = self.table_search.horizontalHeaderItem(1)
        item.setText(_translate("search_form", "Name"))
        item = self.table_search.horizontalHeaderItem(2)
        item.setText(_translate("search_form", "Calories"))
        item = self.table_search.horizontalHeaderItem(3)
        item.setText(_translate("search_form", "Protein"))
        item = self.table_search.horizontalHeaderItem(4)
        item.setText(_translate("search_form", "Carbs"))
        item = self.table_search.horizontalHeaderItem(5)
        item.setText(_translate("search_form", "Sugar"))
        item = self.table_search.horizontalHeaderItem(6)
        item.setText(_translate("search_form", "Fat"))
        item = self.table_search.horizontalHeaderItem(7)
        item.setText(_translate("search_form", "Satfat"))
        item = self.table_search.horizontalHeaderItem(8)
        item.setText(_translate("search_form", "Salt"))
        self.btn_name.setText(_translate("search_form", "Name"))
        self.bnt_barcode.setText(_translate("search_form", "Barcode"))
        self.btn_quit.setText(_translate("search_form", "Quit"))
        self.btn_ok.setText(_translate("search_form", "Ok"))
        self.btn_save.setText(_translate("search_form", "Save"))
        self.btn_new.setText(_translate("search_form", "New"))
        self.btn_remove.setText(_translate("search_form", "Remove"))

