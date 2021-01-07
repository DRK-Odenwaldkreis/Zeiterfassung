#!/usr/bin/python3
# coding=utf-8
import sys
from tkinter import *
from app import App
import sqlite3
from os import path
import logging
from logging.handlers import RotatingFileHandler

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


logFile = 'output.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Main')
logger.debug('Starting')

try:
    init_local_failover_database()
    window.mainloop()
except KeyboardInterrupt():
    logger.warning('Quitting application, received keyboard interrupt')
    sys.exit(0)
except Exception as e:
    logger.error('Setting labels for Messages')
    pass
