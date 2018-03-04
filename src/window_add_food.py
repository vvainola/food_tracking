import gui.add_food_data
import db.databaseHandler
import os
from utils import toggle_keyboard
from PyQt5.QtWidgets import *


class AddFoodWindow(QMainWindow, gui.add_food_data.Ui_add_food_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.parent = parent

        # Connect buttons
        self.btn_cancel.clicked.connect(self.pressed_cancel)
        self.btn_ok.clicked.connect(self.pressed_ok)

        #Callback function to be called on ok press
        self.callback_function = None
        self.callback_arg = None

        # Create message window for errors
        self.error_message = QMessageBox()
        self.error_message.setIcon(QMessageBox.Information)

    def pressed_cancel(self):
        """ Pressing cancel button closes the window
            and keyboard 
        """
        toggle_keyboard("off")
        self.close()

    def pressed_ok(self):
        """ Pressing ok button closes the add food window if all data is filled
        """
        food_data = {}
        for i in range(self.table_food_data.rowCount()):
            row_text = self.table_food_data.item(i, 0).text()
            header_text = self.table_food_data.verticalHeaderItem(
                i).text().upper()
            if row_text == "":
                self.error_message.setText("All data is not filled")
                self.error_message.show()
                return
            else:
                food_data[header_text] = row_text
        # All cells were filled, update db
        db.databaseHandler.replace_into("FOOD_DATA", food_data)

        self.close()
        self.callback_function(self.callback_arg)

    def clear_table(self):
        """ Clear the food data table """
        for i in range(self.table_food_data.rowCount()):
            self.table_food_data.setItem(i, 0, QTableWidgetItem("0"))

    def set_barcode(self, barcode):
        """ Function for presetting the barcode in the table before display """
        self.table_food_data.setItem(0, 0, QTableWidgetItem(barcode))

    def show_window(self, barcode, callback_function, arg):
        # Clear table before showing it
        self.clear_table()

        # Set barcode
        self.set_barcode(barcode)
        self.show()
        self.move(0, 0)

        # Start editing name
        name = self.table_food_data.item(1, 0)
        self.table_food_data.editItem(name)
        self.table_food_data.setCurrentCell(1, 0)

        #Connect callback function
        self.callback_function = callback_function
        self.callback_arg = arg
