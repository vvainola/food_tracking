# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/gui/qt/weight_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_weight_form(object):
    def setupUi(self, weight_form):
        weight_form.setObjectName("weight_form")
        weight_form.resize(204, 169)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(weight_form.sizePolicy().hasHeightForWidth())
        weight_form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        weight_form.setFont(font)
        self.centralwidget = QtWidgets.QWidget(weight_form)
        self.centralwidget.setObjectName("centralwidget")
        self.table_weight = QtWidgets.QTableWidget(self.centralwidget)
        self.table_weight.setGeometry(QtCore.QRect(0, 0, 211, 101))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.table_weight.setFont(font)
        self.table_weight.setObjectName("table_weight")
        self.table_weight.setColumnCount(2)
        self.table_weight.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_weight.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_weight.setHorizontalHeaderItem(1, item)
        self.table_weight.horizontalHeader().setDefaultSectionSize(100)
        self.table_weight.verticalHeader().setVisible(False)
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(20, 110, 71, 51))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(120, 110, 61, 51))
        self.btn_ok.setObjectName("btn_ok")
        weight_form.setCentralWidget(self.centralwidget)

        self.retranslateUi(weight_form)
        QtCore.QMetaObject.connectSlotsByName(weight_form)

    def retranslateUi(self, weight_form):
        _translate = QtCore.QCoreApplication.translate
        weight_form.setWindowTitle(_translate("weight_form", "Weight"))
        item = self.table_weight.horizontalHeaderItem(0)
        item.setText(_translate("weight_form", "Start weight"))
        item = self.table_weight.horizontalHeaderItem(1)
        item.setText(_translate("weight_form", "End weight"))
        self.btn_cancel.setText(_translate("weight_form", "Cancel"))
        self.btn_ok.setText(_translate("weight_form", "Ok"))

