# -*- coding: utf-8 -*-

import sys, signal
from window_main import MainWindow
import db.databaseHandler
from PyQt5.QtWidgets import *

def signal_term_handler(signal, frame): 
    print("got SIGTERM")
    sys.exit(0)
    signal.signal(signal.SIGTERM, signal_term_handler)

if __name__ == '__main__':
    db.databaseHandler.init_database()
    app = QApplication(sys.argv)
    form = MainWindow(app)
    form.show()
    signal.signal(signal.SIGTERM, signal_term_handler)
    sys.exit(app.exec_())
