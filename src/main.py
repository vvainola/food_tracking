# -*- coding: utf-8 -*-

import sys
from window_main import MainWindow
import db.databaseHandler
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    db.databaseHandler.init_database()
    app = QApplication(sys.argv)
    form = MainWindow(app)
    form.show()
    sys.exit(app.exec_())
