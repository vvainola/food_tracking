# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recipe_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_recipe_form(object):
    def setupUi(self, recipe_form):
        recipe_form.setObjectName("recipe_form")
        recipe_form.resize(800, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(recipe_form.sizePolicy().hasHeightForWidth())
        recipe_form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        recipe_form.setFont(font)
        self.centralwidget = QtWidgets.QWidget(recipe_form)
        self.centralwidget.setObjectName("centralwidget")
        self.table_recipe = QtWidgets.QTableWidget(self.centralwidget)
        self.table_recipe.setGeometry(QtCore.QRect(0, 50, 792, 181))
        self.table_recipe.setObjectName("table_recipe")
        self.table_recipe.setColumnCount(9)
        self.table_recipe.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_recipe.setHorizontalHeaderItem(8, item)
        self.table_recipe.horizontalHeader().setDefaultSectionSize(87)
        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.btn_quit.setObjectName("btn_quit")
        self.btn_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_scan.setGeometry(QtCore.QRect(430, 10, 61, 31))
        self.btn_scan.setObjectName("btn_scan")
        self.btn_remove = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remove.setGeometry(QtCore.QRect(560, 10, 81, 31))
        self.btn_remove.setObjectName("btn_remove")
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(490, 10, 71, 31))
        self.btn_search.setObjectName("btn_search")
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(80, 10, 341, 37))
        self.label_name.setObjectName("label_name")
        recipe_form.setCentralWidget(self.centralwidget)

        self.retranslateUi(recipe_form)
        QtCore.QMetaObject.connectSlotsByName(recipe_form)

    def retranslateUi(self, recipe_form):
        _translate = QtCore.QCoreApplication.translate
        recipe_form.setWindowTitle(_translate("recipe_form", "Recipe"))
        item = self.table_recipe.horizontalHeaderItem(0)
        item.setText(_translate("recipe_form", "Name"))
        item = self.table_recipe.horizontalHeaderItem(1)
        item.setText(_translate("recipe_form", "Amount"))
        item = self.table_recipe.horizontalHeaderItem(2)
        item.setText(_translate("recipe_form", "Calories"))
        item = self.table_recipe.horizontalHeaderItem(3)
        item.setText(_translate("recipe_form", "Protein"))
        item = self.table_recipe.horizontalHeaderItem(4)
        item.setText(_translate("recipe_form", "Carbs"))
        item = self.table_recipe.horizontalHeaderItem(5)
        item.setText(_translate("recipe_form", "Sugar"))
        item = self.table_recipe.horizontalHeaderItem(6)
        item.setText(_translate("recipe_form", "Fat"))
        item = self.table_recipe.horizontalHeaderItem(7)
        item.setText(_translate("recipe_form", "Satfat"))
        item = self.table_recipe.horizontalHeaderItem(8)
        item.setText(_translate("recipe_form", "Salt"))
        self.btn_quit.setText(_translate("recipe_form", "Quit"))
        self.btn_scan.setText(_translate("recipe_form", "Scan"))
        self.btn_remove.setText(_translate("recipe_form", "Remove"))
        self.btn_search.setText(_translate("recipe_form", "Search"))
        self.label_name.setText(_translate("recipe_form", "Recipe name"))

