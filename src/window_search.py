import db.databaseHandler
import os
import gui.search_window_auto
from window_recipe import RecipeWindow
from PyQt5.QtWidgets import *


class SearchWindow(QMainWindow, gui.search_window_auto.Ui_search_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        # Set name search by default
        self.btn_name.setChecked(True)

        # Create recipe window
        self.recipe_window = RecipeWindow()

        # Connect buttons
        self.btn_quit.clicked.connect(self.pressed_quit)
        self.btn_ok.clicked.connect(self.pressed_ok)
        self.btn_new.clicked.connect(self.pressed_new)
        self.btn_edit.clicked.connect(self.pressed_edit)
        self.btn_remove.clicked.connect(self.pressed_remove)
        self.btn_save.clicked.connect(self.pressed_save)
        self.box_search.textChanged.connect(self.text_changed)

        #callback function to be called on ok press
        self.cb_function = None

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
        self.parent.update_table_eaten()

    def pressed_remove(self):
        selection_model = self.table_search.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        name = self.table_search.item(row_index, 1).text()
        columns_values = {}
        columns_values["NAME"] = name
        db.databaseHandler.delete_records("FOOD_DATA", columns_values)
        self.table_search.removeRow(row_index)
        self.parent.update_table_eaten()

    def pressed_new(self):
        """ Inserts new item to the end of the search list """
        row_count = self.table_search.rowCount()
        self.table_search.insertRow(row_count)
        # Set barcode as -
        self.table_search.setItem(
            row_count, 0, QTableWidgetItem("-"))
        # Set default values 0
        for i in range(1, self.table_search.columnCount()):
            self.table_search.setItem(
                row_count, i, QTableWidgetItem("0"))
        # Start editing nameo
        name = self.table_search.item(row_count, 1)
        self.table_search.editItem(name)
        self.table_search.setCurrentCell(row_count, 1)

    def pressed_quit(self):
        """ Pressing quit button closes the window """
        os.system("./toggle_keyboard.sh -off")
        self.close()

    def pressed_edit(self):
        """ Pressing edit button opens the recipe window if a row is selected"""
        #Find selected row
        selection_model = self.table_search.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        name = self.table_search.item(row_index, 1).text()

        #Check that a food data exists in database
        search_result = db.databaseHandler.execute("""SELECT *
                                                    FROM FOOD_DATA
                                                    WHERE NAME = ?""",
                                                    (name, ))
        #Food data does not exist, return
        if search_result[1] == []:
            return

        self.close()
        self.recipe_window.show_window(name, self.show_window)

    def pressed_ok(self):
        selection_model = self.table_search.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        name = self.table_search.item(row_index, 1).text()
        self.close()
        self.cb_function(name)

    def text_changed(self):
        self.table_search.setRowCount(0)
        # There is more than 1 character in the search box
        search_text = self.box_search.text()
        if search_text == "":
            search_text = "¤"

        # Search for name
        if self.btn_name.isChecked():
            search_result = db.databaseHandler.search_like(
                "FOOD_DATA", "NAME", search_text)
        # Search for barcode
        else:
            search_result = db.databaseHandler.search_like(
                "FOOD_DATA", "BARCODE", search_text)
        names = search_result[0]
        data = search_result[1]
        # Add search results in the table
        for item in data:
            row_count = self.table_search.rowCount()
            self.table_search.insertRow(row_count)
            self.table_search.setItem(
                row_count, 0, QTableWidgetItem(str(item[names["BARCODE"]])))
            self.table_search.setItem(
                row_count, 1, QTableWidgetItem(str(item[names["NAME"]])))
            self.table_search.setItem(
                row_count, 2, QTableWidgetItem(str(item[names["CALORIES"]])))
            self.table_search.setItem(
                row_count, 3, QTableWidgetItem(str(item[names["PROTEIN"]])))
            self.table_search.setItem(
                row_count, 4, QTableWidgetItem(str(item[names["CARBS"]])))
            self.table_search.setItem(
                row_count, 5, QTableWidgetItem(str(item[names["SUGAR"]])))
            self.table_search.setItem(
                row_count, 6, QTableWidgetItem(str(item[names["FAT"]])))
            self.table_search.setItem(
                row_count, 7, QTableWidgetItem(str(item[names["SATFAT"]])))
            self.table_search.setItem(
                row_count, 8, QTableWidgetItem(str(item[names["SALT"]])))

    def show_window(self, cb_func):
        self.show()
        self.move(0, 0)
        os.system("./toggle_keyboard.sh -on")

        self.cb_function = cb_func
