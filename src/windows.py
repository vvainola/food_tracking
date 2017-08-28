# -*- coding: utf-8 -*-

import os
import db.databaseHandler
import gui.mainwindow_auto
import gui.add_food_data_auto
from barcodescanner import scan_picture
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_scan.clicked.connect(lambda: self.pressed_scan())

        # Create windows
        self.add_food_window = AddFoodWindow()

        # Add total row at the top of the table
        self.table_eaten_today.insertRow(self.table_eaten_today.rowCount())
        self.table_eaten_today.setItem(0, 0, QTableWidgetItem("Today"))
        self.table_eaten_today.setItem(0, 1, QTableWidgetItem("Total"))

    def pressed_scan(self):
        """ Function connected to pressing scan button """
        barcode = scan_picture()
        if barcode != "":
            if (not db.databaseHandler.search("FOOD_DATA", "BARCODE", barcode)):
                # Clear table before showing it
                self.add_food_window.clear_table()
                self.add_food_window.set_barcode(barcode)
                self.add_food_window.show()

                os.system("./toggle_keyboard.sh -on")

class AddFoodWindow(QMainWindow, gui.add_food_data_auto.Ui_add_food_form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_cancel.clicked.connect(lambda: self.pressed_cancel())
        self.btn_ok.clicked.connect(lambda: self.pressed_ok())

        # Create message window for errors
        self.error_message = QMessageBox()
        self.error_message.setIcon(QMessageBox.Information)

    def pressed_cancel(self):
        """ Pressing cancel button closes the window """
        os.system("./toggle_keyboard.sh -off")
        self.close()

    def pressed_ok(self):
        """ Pressing ok button closes the add food window if all data is filled """
        food_data = {}
        for i in range(self.table_food_data.rowCount()):
            row_text = self.table_food_data.item(i, 0).text()
            header_text = self.table_food_data.verticalHeaderItem(i).text()
            if row_text == "":
                self.error_message.setText("All data is not filled")
                self.error_message.show()
                return
            else:
                food_data[header_text] = row_text
        # All cells were filled
        os.system("./toggle_keyboard.sh -off")
        db.databaseHandler.insert_into("FOOD_DATA", food_data)
        self.close()


    def clear_table(self):
        """ Clear the food data table """
        for i in range(self.table_food_data.rowCount()):
            self.table_food_data.setItem(i, 0, QTableWidgetItem(""))

    def set_barcode(self, barcode):
        """ Function for presetting the barcode in the table before display """
        self.table_food_data.setItem(0, 0, QTableWidgetItem(barcode))