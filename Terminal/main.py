#!/usr/bin/python3
# coding=utf-8
import sys
from tkinter import *
from app import App
import sqlite3
from os import path


def init_local_failover_database():
    connection = sqlite3.connect("./Backup.db")
    cursor = connection.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS Dienste (id INTEGER,Hash	Char(64), Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(id AUTOINCREMENT));'''
    cursor.execute(sql)

window = Tk()
window.title("Zeitenbuchungssystem DRK Odenwaldkreis")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(str(width) + "x" + str(height))
#window.config(cursor="none")
app = App(window)
try:
    init_local_failover_database()
    window.mainloop()
except KeyboardInterrupt():
    sys.exit(0)
except:
    pass
