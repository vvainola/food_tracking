# -*- coding: utf-8 -*-

import sys
import windows
import db.databaseHandler
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    db.databaseHandler.init_database()
    app = QApplication(sys.argv)
    form = windows.MainWindow()
    form.show()
    sys.exit(app.exec_())
