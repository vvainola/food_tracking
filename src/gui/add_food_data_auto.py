# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_food_data.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_add_food_form(object):
    def setupUi(self, add_food_form):
        add_food_form.setObjectName("add_food_form")
        add_food_form.resize(184, 454)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(add_food_form.sizePolicy().hasHeightForWidth())
        add_food_form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        add_food_form.setFont(font)
        self.centralwidget = QtWidgets.QWidget(add_food_form)
        self.centralwidget.setObjectName("centralwidget")
        self.table_food_data = QtWidgets.QTableWidget(self.centralwidget)
        self.table_food_data.setGeometry(QtCore.QRect(0, 0, 241, 401))
        self.table_food_data.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.table_food_data.setObjectName("table_food_data")
        self.table_food_data.setColumnCount(1)
        self.table_food_data.setRowCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_food_data.setHorizontalHeaderItem(0, item)
        self.table_food_data.horizontalHeader().setDefaultSectionSize(120)
        self.table_food_data.verticalHeader().setDefaultSectionSize(40)
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(10, 410, 91, 41))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(120, 410, 61, 41))
        self.btn_ok.setObjectName("btn_ok")
        add_food_form.setCentralWidget(self.centralwidget)

        self.retranslateUi(add_food_form)
        QtCore.QMetaObject.connectSlotsByName(add_food_form)

    def retranslateUi(self, add_food_form):
        _translate = QtCore.QCoreApplication.translate
        add_food_form.setWindowTitle(_translate("add_food_form", "Food data"))
        item = self.table_food_data.verticalHeaderItem(0)
        item.setText(_translate("add_food_form", "Barcode"))
        item = self.table_food_data.verticalHeaderItem(1)
        item.setText(_translate("add_food_form", "Name"))
        item = self.table_food_data.verticalHeaderItem(2)
        item.setText(_translate("add_food_form", "Calories"))
        item = self.table_food_data.verticalHeaderItem(3)
        item.setText(_translate("add_food_form", "Protein"))
        item = self.table_food_data.verticalHeaderItem(4)
        item.setText(_translate("add_food_form", "Carbs"))
        item = self.table_food_data.verticalHeaderItem(5)
        item.setText(_translate("add_food_form", "Sugar"))
        item = self.table_food_data.verticalHeaderItem(6)
        item.setText(_translate("add_food_form", "Fat"))
        item = self.table_food_data.verticalHeaderItem(7)
        item.setText(_translate("add_food_form", "Sat fat"))
        item = self.table_food_data.verticalHeaderItem(8)
        item.setText(_translate("add_food_form", "Salt"))
        item = self.table_food_data.horizontalHeaderItem(0)
        item.setText(_translate("add_food_form", "Value"))
        self.btn_cancel.setText(_translate("add_food_form", "Cancel"))
        self.btn_ok.setText(_translate("add_food_form", "Ok"))

