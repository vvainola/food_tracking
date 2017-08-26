# -*- coding: utf-8 -*-


import sys
from barcodescanner import scan_picture
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    scan_picture()

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(800, 480)
    w.move(0, 0)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())