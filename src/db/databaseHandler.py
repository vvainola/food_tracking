# -*- coding: utf-8 -*-

test = False

import sqlite3


def connect_db():
    if test:
        conn = sqlite3.connect('food_tracker_test.db')
    else:
        conn = sqlite3.connect('food_tracker.db')
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_database():
    conn = connect_db()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS FOOD_DATA
                    (ID         INTEGER     PRIMARY KEY,
                    BARCODE     TEXT        DEFAULT '-',
                    NAME        TEXT        UNIQUE      NOT NULL,
                    CALORIES    REAL        DEFAULT 0,
                    CARBS       REAL        DEFAULT 0,
                    SUGAR       REAL        DEFAULT 0,
                    PROTEIN     REAL        DEFAULT 0,
                    FAT         REAL        DEFAULT 0,
                    SATFAT      REAL        DEFAULT 0,
                    SALT        REAL        DEFAULT 0);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS FOOD_LOG
                    (ID         INTEGER     PRIMARY KEY,
                    NAME        TEXT,
                    DATE        TEXT,
                    AMOUNT      INTEGER,
                    CONSTRAINT FK_NAME
                        FOREIGN KEY (NAME) 
                        REFERENCES FOOD_DATA(NAME)
                        ON DELETE CASCADE);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS FOOD_RECIPE
                    (ID         INTEGER     PRIMARY KEY,
                    NAME        TEXT,
                    INGREDIENT  TEXT,
                    AMOUNT      INTEGER,
                    CONSTRAINT FK_INGREDIENT
                        FOREIGN KEY (INGREDIENT) 
                        REFERENCES FOOD_DATA(NAME)
                        ON DELETE CASCADE);''')
    conn.commit()
    conn.close()

def execute(command, values):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(command, values)

    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    names = {}
    for i in range(len(column_names)):
        names[column_names[i]] = i

    # Commit changes
    conn.commit()
    conn.close()

    return (names, data)


def replace_into(table_name, data):
    conn = connect_db()
    exec_text = "REPLACE INTO " + table_name + " ("
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

def insert_into(table_name, data):
    conn = connect_db()
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
    conn = connect_db()
    cursor = conn.cursor()
    exec_text = 'SELECT * FROM ' + table_name + ' WHERE ' + column + '=?'

    # Substitution requires a tuple
    value = (str(value), )
    cursor.execute(exec_text, value)

    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    names = {}
    for i in range(len(column_names)):
        names[column_names[i]] = i

    # Commit changes
    conn.commit()
    conn.close()

    return (names, data)


def search_like(table_name, column, value):
    conn = connect_db()
    cursor = conn.cursor()
    exec_text = 'SELECT * FROM ' + table_name + \
        ' WHERE ' + column + ' LIKE ? COLLATE NOCASE'

    # Substitution requires a tuple
    value = ("%" + str(value) + "%", )
    cursor.execute(exec_text, value)

    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    names = {}
    for i in range(len(column_names)):
        names[column_names[i]] = i
    conn.close()
    return (names, data)


def delete_records(table_name, columns_values):
    """ Function for deleting a record(s) from database with given value """
    conn = connect_db()
    cursor = conn.cursor()
    values = ()
    where_text = ""
    for key, value in columns_values.items():
        where_text = where_text + str(key) +  " = ? AND "
        values = values + (str(value), )
    #Discard the last "AND" and remove only 1 entry
    where_text = where_text[:-4] + " LIMIT 1"
    exec_text = 'DELETE FROM ' + table_name + ' WHERE ' + where_text

    cursor.execute(exec_text, values)

    # Commit changes
    conn.commit()
    conn.close()
