#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Zeiterfassung.

# DRK Zeiterfassung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DRK Zeiterfassung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DRK Zeiterfassung.  If not, see <http://www.gnu.org/licenses/>.


import sys
from tkinter import *
from app import App
import sqlite3
from os import path
import logging
from logging.handlers import RotatingFileHandler
from readconfig import read_config

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
window.config(cursor="none")
app = App(window)


logFile = './Log/output.log'

try:
    logLevel = read_config("Terminal", "logLevel")
    if logLevel == "Error":
        logging.basicConfig(filename=logFile,level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    elif logLevel == "Debug":
        logging.basicConfig(filename=logFile, level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename=logFile, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except:
    logging.basicConfig(filename=logFile, level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
