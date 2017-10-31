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
from PyQt5.QtCore import QThread


class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self, QApp):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.QApp = QApp

        # Connect buttons
        self.btn_scan.clicked.connect(self.pressed_scan)
        self.btn_search.clicked.connect(self.pressed_search)
        self.btn_delete.clicked.connect(self.pressed_delete)

        # Create windows
        self.add_food_window = AddFoodWindow(self)
        self.weight_window = WeightWindow(self)
        self.search_window = SearchWindow(self)

        # Add total row at the top of the table
        self.table_eaten_today.insertRow(self.table_eaten_today.rowCount())
        self.table_eaten_today.setItem(0, 0, QTableWidgetItem("Today"))
        self.table_eaten_today.setItem(0, 1, QTableWidgetItem("Total"))

        # Variables for accessing data across methods
        self.barcode = ""
        self.db_info = ""   # Info found from db
        self.food_name = ""      # Name displayed in weight window
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
                self.food_name = self.db_info["NAME"]
                self.show_weight_window()
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
        # Remove the row quantities from total
        # Calories
        self.total_calories -= float(
            self.table_eaten_today.item(row_index, 3).text())
        # Protein
        self.total_protein -= float(
            self.table_eaten_today.item(row_index, 4).text())
        # Carbs and sugar
        carbs_and_sugar = self.table_eaten_today.item(
            row_index, 5).text().split(" ")
        self.total_carbs -= float(carbs_and_sugar[0])
        self.total_sugar -= float(carbs_and_sugar[1][1:-1])
        # Fat and saturated fat
        fat_and_satfat = self.table_eaten_today.item(
            row_index, 6).text().split(" ")
        self.total_fat -= float(fat_and_satfat[0])
        self.total_satfat -= float(fat_and_satfat[1][1:-1])
        # Salt
        self.total_salt -= float(self.table_eaten_today.item(row_index, 7).text())

        # Update total
        self.update_total()

        # Remove row
        self.table_eaten_today.removeRow(row_index)

    def insert_row(self, weight):
        # After adding a new food, the database info has to be retrieved again
        if self.db_info is None:
            self.search_barcode(self.barcode)

        today = datetime.today()
        today = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        log_entry = {}
        log_entry["NAME"] = self.db_info["NAME"]
        log_entry["DATE"] = today
        log_entry["AMOUNT"] = str(weight)
        db.databaseHandler.replace_into("FOOD_LOG", log_entry)

        # Add a new row at the end of the table
        row_count = self.table_eaten_today.rowCount()
        self.table_eaten_today.insertRow(row_count)
        weight_100 = float(weight) / 100

        # Barcode
        self.table_eaten_today.setItem(
            row_count,   0, QTableWidgetItem(self.db_info["BARCODE"]))
        # Name
        self.table_eaten_today.setItem(
            row_count,   1, QTableWidgetItem(self.db_info["NAME"]))
        # Amount/weight
        self.table_eaten_today.setItem(
            row_count,   2, QTableWidgetItem(str(weight)))
        # Calories
        calories = weight_100 * float(self.db_info["CALORIES"])
        self.total_calories += calories
        self.table_eaten_today.setItem(
            row_count,   3, QTableWidgetItem(str("%.1f" % calories)))
        # Protein
        protein = weight_100 * float(self.db_info["PROTEIN"])
        self.total_protein += protein
        self.table_eaten_today.setItem(
            row_count,   4, QTableWidgetItem(str("%.1f" % protein)))
        # Carbs
        carbs = weight_100 * float(self.db_info["CARBS"])
        self.total_carbs += carbs
        sugar = weight_100 * float(self.db_info["SUGAR"])
        self.total_sugar += sugar
        string = str("%.1f" % carbs) + " (" + str("%.1f" % sugar) + ")"
        self.table_eaten_today.setItem(
            row_count,   5, QTableWidgetItem(string))
        # Fat
        fat = weight_100 * float(self.db_info["FAT"])
        self.total_fat += fat
        satfat = weight_100 * float(self.db_info["SATFAT"])
        self.total_satfat += satfat
        string = str("%.1f" % fat) + " (" + str("%.1f" % satfat) + ")"
        self.table_eaten_today.setItem(
            row_count,   6, QTableWidgetItem(string))
        # Salt
        salt = weight_100 * float(self.db_info["SALT"])
        self.total_salt += salt
        self.table_eaten_today.setItem(
            row_count,   7, QTableWidgetItem(str("%.1f" % salt)))

        # Update total row
        self.update_total()

    def show_add_food_window(self):
        # Clear table before showing it
        self.add_food_window.clear_table()
        self.add_food_window.set_barcode(self.barcode)
        self.add_food_window.show()
        self.add_food_window.move(0, 0)

    def show_weight_window(self):
        # Clear table before showing it
        self.weight_window.setWindowTitle(self.food_name)
        self.weight_window.clear_table()
        self.weight_window.show()
        self.weight_window.move(0, 0)

    def search_barcode(self, barcode):
        """Search database for barcode and save result to db_info"""
        names, data = db.databaseHandler.search(
            "FOOD_DATA", "BARCODE", barcode)
        if data is not None:
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

    def update_total(self):
        """ Method for updating the total row of the today eaten table """
        # Calories
        self.table_eaten_today.setItem(
            0, 3, QTableWidgetItem(str("%.1f" % self.total_calories)))
        # Protein
        self.table_eaten_today.setItem(
            0, 4, QTableWidgetItem(str("%.1f" % self.total_protein)))
        # Carbs and sugar
        total_string = str("%.1f" % self.total_carbs) + \
            " (" + str("%.1f" % self.total_sugar) + ")"
        self.table_eaten_today.setItem(
            0, 5, QTableWidgetItem(total_string))
        # Fat and saturated fat
        total_string = str("%.1f" % self.total_fat) + \
            " (" + str("%.1f" % self.total_satfat) + ")"
        self.table_eaten_today.setItem(
            0, 6, QTableWidgetItem(total_string))
        # Salt
        self.table_eaten_today.setItem(
            0, 7, QTableWidgetItem(str("%.1f" % self.total_salt)))
