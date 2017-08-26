# -*- coding: utf-8 -*-

import sys
import time
import barcodeScanner
from pyzbar.pyzbar import decode
from PIL import Image

def scan_picture():
    """ Scans the picture from rpi camera up to 10 times attempting to read the barcode """
    # Only scan if pi flag is set, so that the app can be run without picamera
    if '-pi' in str(sys.argv):
        import picamera
        camera = picamera.PiCamera()
        camera.rotation = -90
        time.sleep(2)
        camera.start_preview()
        filename = '../data/barcode.png'
        for i in range(10):
            camera.capture(filename)
            barcode = scan_barcode(filename)

            #Return barcode if scan is succesful
            if barcode != "":
                break
        camera.close()
        return barcode

    else:
        print("Camera is not supported")
        return ""

def scan_barcode(filename):
    """Scans barcode from filename image """
    barcode = decode(Image.open(filename))
    # Something was found, assuming that 1st one is correct
    if len(barcode) != 0:
        return barcode[0].data.decode('UTF-8')
    # Nothing was found
    else:
        return ""
