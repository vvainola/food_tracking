# -*- coding: utf-8 -*-

import sys
import gui.mainwindow_auto
import gui.add_food_data_auto
import os
from barcodescanner import scan_picture
from db.databaseHandler import init_database
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow, gui.mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_scan.clicked.connect(self.pressed_scan())

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
            self.add_food_window.show()

class AddFoodWindow(QMainWindow, gui.add_food_data_auto.Ui_add_food_form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Connect buttons
        self.btn_cancel.clicked.connect(self.pressed_cancel())
        self.btn_ok.clicked.connect(self.pressed_ok())

    def pressed_cancel(self):
        """ Pressing cancel button closes the window """
        self.close()

    def pressed_ok(self):
        """ Pressing ok button closes the add food window if data is valid """
        #print(self.table_food_data.rowCount())
        os.system("./toggle_keyboard.sh")
        self.close()


if __name__ == '__main__':
    init_database()
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
