import os 
import gui.weight_window_auto
from PyQt5.QtWidgets import *

class WeightWindow(QMainWindow, gui.weight_window_auto.Ui_weight_form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        # Connect buttons
        self.btn_cancel.clicked.connect(self.pressed_cancel)
        self.btn_ok.clicked.connect(self.pressed_ok)

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