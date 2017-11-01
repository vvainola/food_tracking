# -*- coding: utf-8 -*-

import os
import db.databaseHandler
import gui.mainwindow_auto

from window_add_food import AddFoodWindow
from window_search import SearchWindow
from window_weight import WeightWindow

from barcodescanner import scan_picture
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPoint


class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self, QApp):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.QApp = QApp

        # Date functions
        # Hide calendar by default
        self.calendar.hide()
        #Set date to today on start up
        today = datetime.today()
        self.date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        # Connect buttons
        self.btn_scan.clicked.connect(self.pressed_scan)
        self.btn_search.clicked.connect(self.pressed_search)
        self.btn_delete.clicked.connect(self.pressed_delete)
        self.table_eaten_today.cellClicked.connect(self.dateSelection)

        # Create windows
        self.add_food_window = AddFoodWindow(self)
        self.weight_window = WeightWindow(self)
        self.search_window = SearchWindow(self)

        # Update todays table in case program had been closed
        self.update_table_eaten()

        # Variables for accessing data across methods
        self.barcode = ""
        self.db_info = ""   # Info found from db

    def pressed_scan(self):
        """ Function connected to pressing scan button """
        # Disconnect scan button so that multiple scans
        # do not occur in a row
        self.btn_scan.disconnect()

        self.barcode = scan_picture()
        if self.barcode != "":
            self.search_barcode(self.barcode)
            # No data exists yet, create new food
            if self.db_info is None:
                self.show_add_food_window()
            # Go directly to weighing
            else:
                self.show_weight_window(self.db_info["NAME"])
            os.system("./toggle_keyboard.sh -on")

        # Process events until all disconnected scans
        # are processed
        while self.QApp.hasPendingEvents():
            self.QApp.processEvents()
        self.btn_scan.clicked.connect(self.pressed_scan)

    def pressed_search(self):
        self.search_window.show()
        self.search_window.move(0, 0)
        os.system("./toggle_keyboard.sh -on")

    def pressed_delete(self):
        selection_model = self.table_eaten_today.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        name = self.table_eaten_today.item(row_index, 1).text()
        amount = self.table_eaten_today.item(row_index, 2).text()

        # Remove row from food log
        columns_values = {}
        columns_values["NAME"] = name
        columns_values["AMOUNT"] = amount
        db.databaseHandler.delete_records("FOOD_LOG", columns_values)

        self.update_table_eaten()

    def insert_row(self, weight):
        # After adding a new food, the database info has to be retrieved again
        if self.db_info is None:
            self.search_barcode(self.barcode)

        log_entry = {}
        log_entry["NAME"] = self.db_info["NAME"]
        log_entry["DATE"] = self.date
        log_entry["AMOUNT"] = str(weight)
        db.databaseHandler.replace_into("FOOD_LOG", log_entry)

        # Update total row
        self.update_table_eaten()

    def show_add_food_window(self):
        # Clear table before showing it
        self.add_food_window.clear_table()
        # Set barcode
        self.add_food_window.set_barcode(self.barcode)
        self.add_food_window.show()
        self.add_food_window.move(0, 0)

        # Start editing name
        name = self.add_food_window.table_food_data.item(1, 0)
        print(name.text())
        self.add_food_window.table_food_data.editItem(name)

    def show_weight_window(self, title):
        """ Display weight window

        Args:
            name: window title text
        """
        self.weight_window.setWindowTitle(title)
        # Clear table before showing it
        self.weight_window.clear_table()
        self.weight_window.show()
        self.weight_window.move(0, 0)

        # Start editing start weight
        start_weight = self.weight_window.table_weight.item(0, 0)
        self.weight_window.table_weight.editItem(start_weight)

    def search_barcode(self, barcode):
        """ Search database for barcode and update
        internal db info data

        Args:
            barcode: The barcode to be searched
        """
        self.db_info = None
        names, data = db.databaseHandler.search(
            "FOOD_DATA", "BARCODE", barcode)
        if data != []:
            data = data[0]
            self.db_info = {}
            self.db_info["BARCODE"] = data[names["BARCODE"]]
            self.db_info["NAME"] = data[names["NAME"]]
            self.db_info["CALORIES"] = data[names["CALORIES"]]
            self.db_info["PROTEIN"] = data[names["PROTEIN"]]
            self.db_info["CARBS"] = data[names["CARBS"]]
            self.db_info["SUGAR"] = data[names["SUGAR"]]
            self.db_info["FAT"] = data[names["FAT"]]
            self.db_info["SATFAT"] = data[names["SATFAT"]]
            self.db_info["SALT"] = data[names["SALT"]]

    def search_name(self, name):
        self.db_info = None
        """Search database for name and save result to db_info"""
        names, data = db.databaseHandler.search(
            "FOOD_DATA", "NAME", name)
        data = data[0]
        if data is not None:
            self.db_info = {}
            self.db_info["BARCODE"] = data[names["BARCODE"]]
            self.db_info["NAME"] = data[names["NAME"]]
            self.db_info["CALORIES"] = data[names["CALORIES"]]
            self.db_info["PROTEIN"] = data[names["PROTEIN"]]
            self.db_info["CARBS"] = data[names["CARBS"]]
            self.db_info["SUGAR"] = data[names["SUGAR"]]
            self.db_info["FAT"] = data[names["FAT"]]
            self.db_info["SATFAT"] = data[names["SATFAT"]]
            self.db_info["SALT"] = data[names["SALT"]]

    def update_table_eaten(self):
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_sugar = 0
        total_fat = 0
        total_satfat = 0
        total_salt = 0

        #Search food log entries for selected date       
        log_columns, log_data = db.databaseHandler.search(
            "FOOD_LOG", "DATE", self.date)

        # Insert total row
        self.table_eaten_today.setRowCount(0)
        row_count = self.table_eaten_today.rowCount()
        self.table_eaten_today.insertRow(row_count)
        self.table_eaten_today.setItem(row_count, 0, QTableWidgetItem(self.date))
        self.table_eaten_today.setItem(row_count, 1, QTableWidgetItem("Total"))
        if log_data is not None:
            for log_entry in log_data:
                food_columns, food_data = db.databaseHandler.search(
                    "FOOD_DATA", "NAME", log_entry[log_columns["NAME"]])

                # Names are unique so only one entry is retrieved
                food_data = food_data[0]

                # Add new row
                row_count = self.table_eaten_today.rowCount()
                self.table_eaten_today.insertRow(row_count)

                weight = log_entry[log_columns["AMOUNT"]]
                weight_100 = float(weight) / 100

                # Barcode
                self.table_eaten_today.setItem(
                    row_count, 0, QTableWidgetItem(food_data[food_columns["BARCODE"]]))

                # Name
                self.table_eaten_today.setItem(
                    row_count, 1, QTableWidgetItem(food_data[food_columns["NAME"]]))

                # Amount/weight
                self.table_eaten_today.setItem(
                    row_count, 2, QTableWidgetItem(str(weight)))

                # Calories
                calories = weight_100 * \
                    float(food_data[food_columns["CALORIES"]])
                total_calories += calories
                self.table_eaten_today.setItem(
                    row_count, 3, QTableWidgetItem(str("%.1f" % calories)))

                # Protein
                protein = weight_100 * \
                    float(food_data[food_columns["PROTEIN"]])
                total_protein += protein
                self.table_eaten_today.setItem(
                    row_count, 4, QTableWidgetItem(str("%.1f" % protein)))

                # Carbs
                carbs = weight_100 * float(food_data[food_columns["CARBS"]])
                total_carbs += carbs
                sugar = weight_100 * float(food_data[food_columns["SUGAR"]])
                total_sugar += sugar
                string = str("%.1f" % carbs) + " (" + str("%.1f" % sugar) + ")"
                self.table_eaten_today.setItem(
                    row_count, 5, QTableWidgetItem(string))

                # Fat
                fat = weight_100 * float(food_data[food_columns["FAT"]])
                total_fat += fat
                satfat = weight_100 * float(food_data[food_columns["SATFAT"]])
                total_satfat += satfat
                string = str("%.1f" % fat) + " (" + str("%.1f" % satfat) + ")"
                self.table_eaten_today.setItem(
                    row_count, 6, QTableWidgetItem(string))

                # Salt
                salt = weight_100 * float(food_data[food_columns["SALT"]])
                total_salt += salt
                self.table_eaten_today.setItem(
                    row_count, 7, QTableWidgetItem(str("%.1f" % salt)))

        # Update total row
        # Calories
        self.table_eaten_today.setItem(
            0, 3, QTableWidgetItem(str("%.1f" % total_calories)))
        # Protein
        self.table_eaten_today.setItem(
            0, 4, QTableWidgetItem(str("%.1f" % total_protein)))
        # Carbs and sugar
        total_string = str("%.1f" % total_carbs) + \
            " (" + str("%.1f" % total_sugar) + ")"
        self.table_eaten_today.setItem(
            0, 5, QTableWidgetItem(total_string))
        # Fat and saturated fat
        total_string = str("%.1f" % total_fat) + \
            " (" + str("%.1f" % total_satfat) + ")"
        self.table_eaten_today.setItem(
            0, 6, QTableWidgetItem(total_string))
        # Salt
        self.table_eaten_today.setItem(
            0, 7, QTableWidgetItem(str("%.1f" % total_salt)))

    def dateSelection(self, row, column):
        if row == 0 and column == 0 and self.calendar.isHidden:
            self.calendar.show()
        else:
            date = self.calendar.selectedDate()
            day = date.day()
            month = date.month()
            year = date.year()
            self.date = str(year) + "-" + str(month) + "-" + str(day)
            self.update_table_eaten()
            self.calendar.hide()
