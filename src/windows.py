# -*- coding: utf-8 -*-

import os
import db.databaseHandler
import gui.mainwindow_auto
import gui.add_food_data_auto
import gui.weight_window_auto
from barcodescanner import scan_picture
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_scan.clicked.connect(lambda: self.pressed_scan())

        # Create windows
        self.add_food_window = AddFoodWindow(self)
        self.weight_window = WeightWindow(self)

        # Add total row at the top of the table
        self.table_eaten_today.insertRow(self.table_eaten_today.rowCount())
        self.table_eaten_today.setItem(0, 0, QTableWidgetItem("Today"))
        self.table_eaten_today.setItem(0, 1, QTableWidgetItem("Total"))

        # Variables for accessing data across methods
        self.db_info = ""   # Info found from db
        self.weight = ""    # Measured weight
        self.total_calories = 0
        self.total_protein = 0
        self.total_carbs = 0
        self.total_sugar = 0
        self.total_fat = 0
        self.total_satfat = 0
        self.total_salt = 0

    def pressed_scan(self):
        """ Function connected to pressing scan button """
        barcode = scan_picture()
        if barcode != "":
            self.db_info = db.databaseHandler.search("FOOD_DATA", "BARCODE", barcode)
            if (self.db_info is None):
                self.show_add_food_window()
            else:
                self.show_weight_window()
            os.system("./toggle_keyboard.sh -on")

    def insert_row(self, weight):
        row_count = self.table_eaten_today.rowCount()
        self.table_eaten_today.insertRow(row_count)
        weight_100 = float(weight) / 100

        # Barcode
        self.table_eaten_today.setItem(row_count,   0, QTableWidgetItem(self.db_info[1]))
        # Name
        self.table_eaten_today.setItem(row_count,   1, QTableWidgetItem(self.db_info[2]))
        # Amount/weight
        self.table_eaten_today.setItem(row_count,   2, QTableWidgetItem(str(weight)))
        # Calories
        calories = weight_100 * float(self.db_info[3])
        self.total_calories += calories
        self.table_eaten_today.setItem(0,           3, QTableWidgetItem(str("%.1f" % self.total_calories)))
        self.table_eaten_today.setItem(row_count,   3, QTableWidgetItem(str("%.1f" % calories)))
        # Protein
        protein = weight_100 * float(self.db_info[4])
        self.total_protein += protein
        self.table_eaten_today.setItem(0,           4, QTableWidgetItem(str("%.1f" % self.total_protein)))
        self.table_eaten_today.setItem(row_count,   4, QTableWidgetItem(str("%.1f" % protein)))
        # Carbs
        carbs = weight_100 * float(self.db_info[5])
        self.total_carbs += carbs
        sugar = weight_100 * float(self.db_info[6])
        self.total_sugar += sugar
        string = str("%.1f" % carbs) + " (" + str("%.1f" % sugar) + ")"
        total_string = str("%.1f" % self.total_carbs) + " (" + str("%.1f" % self.total_sugar) + ")"
        self.table_eaten_today.setItem(0,           5, QTableWidgetItem(total_string))
        self.table_eaten_today.setItem(row_count,   5, QTableWidgetItem(string))
        # Fat
        fat = weight_100 * float(self.db_info[7])
        self.total_fat += fat
        satfat = weight_100 * float(self.db_info[8])
        self.total_satfat += satfat
        string = str("%.1f" % fat) + " (" + str("%.1f" % satfat) + ")"
        total_string = str("%.1f" % self.total_fat) + " (" + str("%.1f" % self.total_satfat) + ")"
        self.table_eaten_today.setItem(0,           6, QTableWidgetItem(total_string))
        self.table_eaten_today.setItem(row_count,   6, QTableWidgetItem(string))
        # Salt
        salt = weight_100 * float(self.db_info[9])
        self.total_salt += salt
        self.table_eaten_today.setItem(0,           7, QTableWidgetItem(str("%.1f" % self.total_salt)))
        self.table_eaten_today.setItem(row_count,   7, QTableWidgetItem(str("%.1f" % salt)))


    def show_add_food_window(self):
        # Clear table before showing it
        self.add_food_window.clear_table()
        self.add_food_window.set_barcode(self.barcode)
        self.add_food_window.show()
    
    def show_weight_window(self):
        # Clear table before showing it
        self.weight_window.clear_table()
        self.weight_window.show()

class AddFoodWindow(QMainWindow, gui.add_food_data_auto.Ui_add_food_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parent = parent

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

class WeightWindow(QMainWindow, gui.weight_window_auto.Ui_weight_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        # Connect buttons
        self.btn_cancel.clicked.connect(lambda: self.pressed_cancel())
        self.btn_ok.clicked.connect(lambda: self.pressed_ok())

        # Add row for start and end weights
        self.table_weight.insertRow(0)

    def pressed_cancel(self):
        """ Pressing cancel button closes the window """
        os.system("./toggle_keyboard.sh -off")
        self.close()

    def pressed_ok(self):
        """ Pressing ok button closes the window and add the values to todays table """
        os.system("./toggle_keyboard.sh -off")
        start_weight = int(self.table_weight.item(0, 0).text())
        end_weight = int(self.table_weight.item(0, 1).text())
        weight = start_weight - end_weight

        # Insert row to main window and close weight window
        self.parent.insert_row(weight)
        self.close()

    def clear_table(self):
        """ Clear the food data table """
        self.table_weight.setItem(0, 0, QTableWidgetItem("0"))
        self.table_weight.setItem(0, 1, QTableWidgetItem("0"))
