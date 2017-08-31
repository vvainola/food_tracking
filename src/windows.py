# -*- coding: utf-8 -*-

import os
import db.databaseHandler
import gui.mainwindow_auto
import gui.add_food_data_auto
import gui.weight_window_auto
import gui.search_window_auto
from barcodescanner import scan_picture
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_scan.clicked.connect(lambda: self.pressed_scan())
        self.btn_search.clicked.connect(lambda: self.pressed_search())
        self.btn_delete.clicked.connect(lambda: self.pressed_delete())

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
        self.barcode = scan_picture()
        if self.barcode != "":
            self.search_barcode(self.barcode)
            if (self.db_info is None):
                self.show_add_food_window()
            else:
                self.show_weight_window()
            os.system("./toggle_keyboard.sh -on")
        
    def pressed_search(self):
        self.search_window.show()
        os.system("./toggle_keyboard.sh -on")

    def pressed_delete(self):
        selection_model = self.table_eaten_today.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        # Remove the row quantities from total
        # Calories
        self.total_calories -= float(self.table_eaten_today.item(row_index, 3).text())
        # Protein
        self.total_protein -= float(self.table_eaten_today.item(row_index, 4).text())
        # Carbs and sugar
        carbs_and_sugar = self.table_eaten_today.item(row_index, 5).text().split(" ")
        self.total_carbs -= float(carbs_and_sugar[0])
        self.total_sugar -= float(carbs_and_sugar[1][1:-1])
        # Fat and saturated fat
        fat_and_satfat = self.table_eaten_today.item(row_index, 6).text().split(" ")
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

        # Add a new row at the end of the table    
        row_count = self.table_eaten_today.rowCount()
        self.table_eaten_today.insertRow(row_count)
        weight_100 = float(weight) / 100

        # Barcode
        self.table_eaten_today.setItem(row_count,   0, QTableWidgetItem(self.db_info["BARCODE"]))
        # Name
        self.table_eaten_today.setItem(row_count,   1, QTableWidgetItem(self.db_info["NAME"]))
        # Amount/weight
        self.table_eaten_today.setItem(row_count,   2, QTableWidgetItem(str(weight)))
        # Calories
        calories = weight_100 * float(self.db_info["CALORIES"])
        self.total_calories += calories
        self.table_eaten_today.setItem(row_count,   3, QTableWidgetItem(str("%.1f" % calories)))
        # Protein
        protein = weight_100 * float(self.db_info["PROTEIN"])
        self.total_protein += protein
        self.table_eaten_today.setItem(row_count,   4, QTableWidgetItem(str("%.1f" % protein)))
        # Carbs
        carbs = weight_100 * float(self.db_info["CARBS"])
        self.total_carbs += carbs
        sugar = weight_100 * float(self.db_info["SUGAR"])
        self.total_sugar += sugar
        string = str("%.1f" % carbs) + " (" + str("%.1f" % sugar) + ")"  
        self.table_eaten_today.setItem(row_count,   5, QTableWidgetItem(string))
        # Fat
        fat = weight_100 * float(self.db_info["FAT"])
        self.total_fat += fat
        satfat = weight_100 * float(self.db_info["SATFAT"])
        self.total_satfat += satfat
        string = str("%.1f" % fat) + " (" + str("%.1f" % satfat) + ")"
        self.table_eaten_today.setItem(row_count,   6, QTableWidgetItem(string))
        # Salt
        salt = weight_100 * float(self.db_info["SALT"])
        self.total_salt += salt
        self.table_eaten_today.setItem(row_count,   7, QTableWidgetItem(str("%.1f" % salt)))

        # Update total row
        self.update_total()


    def show_add_food_window(self):
        # Clear table before showing it
        self.add_food_window.clear_table()
        self.add_food_window.set_barcode(self.barcode)
        self.add_food_window.show()
    
    def show_weight_window(self):
        # Clear table before showing it
        self.weight_window.clear_table()
        self.weight_window.show()

    def search_barcode(self, barcode):
        """ Function for searching database for the barcode and saving result to memory """
        self.db_info = db.databaseHandler.search("FOOD_DATA", "BARCODE", barcode)

    def update_total(self):
        """ Method for updating the total row of the today eaten table """
        # Calories
        self.table_eaten_today.setItem(0,           3, QTableWidgetItem(str("%.1f" % self.total_calories)))
        # Protein
        self.table_eaten_today.setItem(0,           4, QTableWidgetItem(str("%.1f" % self.total_protein)))
        # Carbs and sugar
        total_string = str("%.1f" % self.total_carbs) + " (" + str("%.1f" % self.total_sugar) + ")"
        self.table_eaten_today.setItem(0,           5, QTableWidgetItem(total_string))
        # Fat and saturated fat
        total_string = str("%.1f" % self.total_fat) + " (" + str("%.1f" % self.total_satfat) + ")"
        self.table_eaten_today.setItem(0,           6, QTableWidgetItem(total_string))
        # Salt
        self.table_eaten_today.setItem(0,           7, QTableWidgetItem(str("%.1f" % self.total_salt)))


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
        db.databaseHandler.replace_into("FOOD_DATA", food_data)
        self.close()
        self.parent.show_weight_window()

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

class SearchWindow(QMainWindow, gui.search_window_auto.Ui_search_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        # Set name search by default
        self.btn_name.setChecked(True)

        # Connect buttons
        self.btn_quit.clicked.connect(lambda: self.pressed_quit())
        self.btn_ok.clicked.connect(lambda: self.pressed_ok())
        self.btn_new.clicked.connect(lambda: self.pressed_new())
        self.btn_remove.clicked.connect(lambda: self.pressed_remove())
        self.btn_save.clicked.connect(lambda: self.pressed_save())
        self.box_search.textChanged.connect(lambda: self.text_changed())

    def pressed_save(self):
        # Go through all rows
        for i in range(self.table_search.rowCount()):
            food_data = {}
            # All columns
            for j in range(self.table_search.columnCount()):
                column_text = self.table_search.item(i, j).text()
                header_text = self.table_search.horizontalHeaderItem(j).text()
                food_data[header_text] = str(column_text)
            # Update database after each row
            db.databaseHandler.replace_into("FOOD_DATA", food_data)

    def pressed_remove(self):
        """ TODO """
        selection_model = self.table_search.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        name = self.table_search.item(row_index, 1).text()
        db.databaseHandler.delete_record("FOOD_DATA", "NAME", name)
        self.table_search.removeRow(row_index)

    def pressed_new(self):
        """ Inserts new item to the end of the search list """
        row_count = self.table_search.rowCount()
        self.table_search.insertRow(row_count)

    def pressed_quit(self):
        """ Pressing quit button closes the window """
        os.system("./toggle_keyboard.sh -off")
        self.close()

    def pressed_ok(self):
        selection_model = self.table_search.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        barcode = self.table_search.item(row_index, 0).text()
        self.parent.search_barcode(barcode)
        self.close()
        self.parent.show_weight_window()

    def text_changed(self):
        self.table_search.setRowCount(0)
        # There is more than 1 character in the search box
        search_text = self.box_search.text()
        if search_text == "":
            search_text = "-"

        # Search for name
        if self.btn_name.isChecked():
            search_result = db.databaseHandler.search_like("FOOD_DATA", "NAME", search_text)
        # Search for barcode
        else:
            search_result = db.databaseHandler.search_like("FOOD_DATA", "BARCODE", search_text)
        names = search_result[0]
        data = search_result[1]
        # Add search results in the table
        for item in data:
            row_count = self.table_search.rowCount()
            self.table_search.insertRow(row_count)
            self.table_search.setItem(row_count, 0, QTableWidgetItem(str(item[names["BARCODE"]])))
            self.table_search.setItem(row_count, 1, QTableWidgetItem(str(item[names["NAME"]])))
            self.table_search.setItem(row_count, 2, QTableWidgetItem(str(item[names["CALORIES"]])))
            self.table_search.setItem(row_count, 3, QTableWidgetItem(str(item[names["PROTEIN"]])))
            self.table_search.setItem(row_count, 4, QTableWidgetItem(str(item[names["CARBS"]])))
            self.table_search.setItem(row_count, 5, QTableWidgetItem(str(item[names["SUGAR"]])))
            self.table_search.setItem(row_count, 6, QTableWidgetItem(str(item[names["FAT"]])))
            self.table_search.setItem(row_count, 7, QTableWidgetItem(str(item[names["SATFAT"]])))
            self.table_search.setItem(row_count, 8, QTableWidgetItem(str(item[names["SALT"]])))
