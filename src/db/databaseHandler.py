# -*- coding: utf-8 -*-

import sqlite3

def init_database():
    conn = sqlite3.connect('food_tracker.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS FOOD_DATA
                    (ID         INT     PRIMARY KEY     NOT NULL,
                    BARCODE     TEXT,
                    NAME        TEXT                    NOT NULL,
                    CALORIES    REAL,
                    CARBS       REAL,
                    SUGAR       REAL,
                    PROTEIN     REAL,
                    FAT         REAL,
                    SATFAT      REAL);''')
    conn.commit()
    conn.close()
