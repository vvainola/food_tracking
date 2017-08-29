# -*- coding: utf-8 -*-

import sqlite3

def init_database():
    conn = sqlite3.connect('food_tracker.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS FOOD_DATA
                    (ID         INTEGER     PRIMARY KEY,
                    BARCODE     TEXT,
                    NAME        TEXT,
                    CALORIES    REAL,
                    CARBS       REAL,
                    SUGAR       REAL,
                    PROTEIN     REAL,
                    FAT         REAL,
                    SATFAT      REAL,
                    SALT        REAL);''')
    conn.commit()
    conn.close()

def insert_into(table_name, data):
    conn = sqlite3.connect('food_tracker.db')
    exec_text = "INSERT INTO " + table_name + " ("
    columns = ""
    values_text = ""
    # Actual values are kept separate to avoid SQL injection
    values = []
    for key, value in data.items():
        # Columns cannot have spaces in them
        columns += " " + key.replace(" ", "") + ", "
        values_text += " ?, "
        values.append(value)
    # Remove last comma by removing 2 last characters
    columns = columns[:-2]
    values_text = values_text[:-2]

    # Combine the whole text and execute
    exec_text = exec_text + columns + ") VALUES (" + values_text + ");"
    # Values replace the question marks
    conn.execute(exec_text, tuple(values))

    # Commit changes
    conn.commit()
    conn.close()

def search(table_name, column, value):
    conn = sqlite3.connect('food_tracker.db')
    cursor = conn.cursor()
    exec_text = 'SELECT * FROM ' + table_name +  ' WHERE ' + column + '=?'

    #Substitution requires a tuple
    value = (str(value), )
    cursor.execute(exec_text, value)
    result = cursor.fetchone()

    # Commit changes
    conn.commit()
    conn.close()

    return result
