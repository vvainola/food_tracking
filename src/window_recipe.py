import db.databaseHandler
import gui.recipe_window
import time
import os
import window_search

from window_weight import WeightWindow

from barcodescanner import scan_picture
from utils import toggle_keyboard

from PyQt5.QtWidgets import *


class RecipeWindow(QMainWindow, gui.recipe_window.Ui_recipe_form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_quit.clicked.connect(self.pressed_quit)
        self.btn_remove.clicked.connect(self.pressed_remove)
        self.btn_scan.clicked.connect(self.pressed_scan)
        self.btn_search.clicked.connect(self.pressed_search)

        #Create windows
        self.weight_window = WeightWindow()
        self.search_window = window_search.SearchWindow(recipe_window=False)

        # Name of the recipe
        self.name = None
        self.ingredient_name = ""

        self.calories_100 = 0
        self.carbs_100 = 0
        self.sugar_100 = 0
        self.protein_100 = 0
        self.fat_100 = 0
        self.satfat_100 = 0
        self.salt_100 = 0

        #Set column widths
        self.table_recipe.setColumnWidth(0, 200) # Name
        self.table_recipe.setColumnWidth(1, 72) # Amount
        self.table_recipe.setColumnWidth(2, 72) # Calories
        self.table_recipe.setColumnWidth(3, 72) # Protein
        self.table_recipe.setColumnWidth(4, 72) # Carbs
        self.table_recipe.setColumnWidth(5, 72) # Sugar
        self.table_recipe.setColumnWidth(6, 72) # Fat
        self.table_recipe.setColumnWidth(7, 72) # Satfat
        self.table_recipe.setColumnWidth(8, 72) # Salt

    def pressed_quit(self):
        self.close()

    def pressed_remove(self):
        selection_model = self.table_recipe.selectionModel()
        try:
            row_index = selection_model.selectedRows()[0].row()
        except IndexError:
            return
        ingredient = self.table_recipe.item(row_index, 0).text()
        amount = self.table_recipe.item(row_index, 1).text()
        columns_values = {}
        columns_values["NAME"] = self.name
        columns_values["INGREDIENT"] = ingredient
        columns_values["AMOUNT"] = amount
        db.databaseHandler.delete_records("FOOD_RECIPE", columns_values)
        self.table_recipe.removeRow(row_index)
        self.update_table()

    def pressed_search(self):
        self.search_window.show_window(self.add_name_ingredient)

    def pressed_scan(self):
        barcode = scan_picture()
        if barcode != "":
            columns, data = db.databaseHandler.execute(
                """SELECT *
                FROM FOOD_DATA
                WHERE BARCODE=?""",
                (barcode,)
            )
            if data != []:
                self.ingredient_name = data[0][columns["NAME"]]
                self.weight_window.show_window(self.add_ingredient)

    def add_name_ingredient(self, ingredient_name):
        self.show_window(self.name)
        self.ingredient_name = ingredient_name
        self.weight_window.show_window(self.add_ingredient)

    def add_ingredient(self, weight):
        data = {}
        data["NAME"] = self.name
        data["INGREDIENT"] = self.ingredient_name
        data["AMOUNT"] = weight
        db.databaseHandler.insert_into("FOOD_RECIPE", data)
        self.update_table(update_database=True)

    def show_window(self, name):
        self.show()
        self.label_name.setText(name)
        self.setGeometry(self.geometry())
        self.move(0, 0)

        self.name = name
        self.update_table()

    def update_table(self, update_database=False):
        # Reset total values
        total_amount = 0
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_sugar = 0
        total_fat = 0
        total_satfat = 0
        total_salt = 0

        #Empty table
        self.table_recipe.setRowCount(0)

        # Insert per 100g row
        self.table_recipe.insertRow(0)
        self.table_recipe.setItem(
            0, 0, QTableWidgetItem("Per 100g"))

        # Insert total row
        self.table_recipe.insertRow(1)
        self.table_recipe.setItem(
            1, 0, QTableWidgetItem("Total"))

        # Find existing ingredients of the recipe
        recipe_columns, recipe = db.databaseHandler.execute(
            """SELECT *
            FROM FOOD_RECIPE
            WHERE NAME = ?""",
            (self.name,))
        for ingredient in recipe:
            columns, data = db.databaseHandler.execute(
                """SELECT *
                FROM FOOD_DATA
                WHERE NAME = ?""",
                (ingredient[recipe_columns["INGREDIENT"]],))
            #The data is a tuple, only first one is used
            data = data[0]

            #Create new row
            row_count = self.table_recipe.rowCount()
            self.table_recipe.insertRow(row_count)

            weight = float(ingredient[recipe_columns["AMOUNT"]])
            weight_100 = float(weight) / 100

            #Name
            self.table_recipe.setItem(
                row_count, 0, QTableWidgetItem(data[columns["NAME"]]))
            
            #Amount/weight
            total_amount += weight
            self.table_recipe.setItem(
                row_count, 1, QTableWidgetItem(str(weight)))

            #Calories
            calories = weight_100 * float(data[columns["CALORIES"]])
            total_calories += calories
            self.table_recipe.setItem(
                row_count, 2, QTableWidgetItem(str("%.1f" % calories)))

            #Protein
            protein = weight_100 * float(data[columns["PROTEIN"]])
            total_protein += protein
            self.table_recipe.setItem(
                row_count, 3, QTableWidgetItem(str("%.1f" % protein)))

            #Carbs
            carbs = weight_100 * float(data[columns["CARBS"]])
            total_carbs += carbs
            self.table_recipe.setItem(
                row_count, 4, QTableWidgetItem(str("%.1f" % carbs)))

            #Sugar
            sugar = weight_100 * float(data[columns["SUGAR"]])
            total_sugar += sugar
            self.table_recipe.setItem(
                row_count, 5, QTableWidgetItem(str("%.1f" % sugar)))

            #Fat
            fat = weight_100 * float(data[columns["FAT"]])
            total_fat += fat
            self.table_recipe.setItem(
                row_count, 6, QTableWidgetItem(str("%.1f" % fat)))

            #Satfat
            satfat = weight_100 * float(data[columns["SATFAT"]])
            total_satfat += satfat
            self.table_recipe.setItem(
                row_count, 7, QTableWidgetItem(str("%.1f" % satfat)))

            #Salt
            salt = weight_100 * float(data[columns["SALT"]])
            total_salt += salt
            self.table_recipe.setItem(
                row_count, 8, QTableWidgetItem(str("%.1f" % salt)))

        recipe_data = {}
        recipe_data["NAME"] = self.name
        #Update per 100g and total rows
        if total_amount == 0:
            total_amount = 1
        weight_100 = total_amount/100
        #Amount
        self.table_recipe.setItem(
            0, 1, QTableWidgetItem(str("%.1f" % 100)))
        self.table_recipe.setItem(
            1, 1, QTableWidgetItem(str("%.1f" % total_amount)))
        #Calories
        calories_100 = round(total_calories / weight_100,1)
        recipe_data["CALORIES"] = calories_100
        self.table_recipe.setItem(
            0, 2, QTableWidgetItem(str("%.1f" % calories_100)))
        self.table_recipe.setItem(
            1, 2, QTableWidgetItem(str("%.1f" % total_calories)))
        #Protein
        protein_100 = round(total_protein/weight_100,1)
        recipe_data["PROTEIN"] = protein_100
        self.table_recipe.setItem(
            0, 3, QTableWidgetItem(str("%.1f" % protein_100)))
        self.table_recipe.setItem(
            1, 3, QTableWidgetItem(str("%.1f" % total_protein)))
        #Carbs
        carbs_100 = round(total_carbs/weight_100,1)
        recipe_data["CARBS"] = carbs_100
        self.table_recipe.setItem(
            0, 4, QTableWidgetItem(str("%.1f" % carbs_100)))
        self.table_recipe.setItem(
            1, 4, QTableWidgetItem(str("%.1f" % total_carbs)))
        #Sugar
        sugar_100 = round(total_sugar/weight_100,1)
        recipe_data["SUGAR"] = sugar_100
        self.table_recipe.setItem(
            0, 5, QTableWidgetItem(str("%.1f" % sugar_100)))
        self.table_recipe.setItem(
            1, 5, QTableWidgetItem(str("%.1f" % total_sugar)))
        #Fat
        fat_100 = round(total_fat/weight_100,1)
        recipe_data["FAT"] = fat_100
        self.table_recipe.setItem(
            0, 6, QTableWidgetItem(str("%.1f" % fat_100)))
        self.table_recipe.setItem(
            1, 6, QTableWidgetItem(str("%.1f" % total_satfat)))
        #Satfat
        satfat_100 = round(total_satfat/weight_100,1)
        recipe_data["SATFAT"] = satfat_100
        self.table_recipe.setItem(
            0, 7, QTableWidgetItem(str("%.1f" % satfat_100)))
        self.table_recipe.setItem(
            1, 7, QTableWidgetItem(str("%.1f" % total_satfat)))
        #Salt
        salt_100 = round(total_salt/weight_100,1)
        recipe_data["SALT"] = salt_100
        self.table_recipe.setItem(
            0, 8, QTableWidgetItem(str("%.1f" % salt_100)))
        self.table_recipe.setItem(
            1, 8, QTableWidgetItem(str("%.1f" % total_salt)))

        if update_database:
            db.databaseHandler.replace_into("FOOD_DATA", recipe_data)


