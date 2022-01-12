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


from datetime import datetime, timedelta
import sys
from tkinter import *
from app import App
import requests
import json
import sqlite3
from os import path,makedirs
import logging
from logging.handlers import RotatingFileHandler
from utils.readconfig import read_config
from utils.failoverdatabase import init_local_failover_database
from utils.token import request_token,check_token

window = Tk()
try:
    window.title(read_config('Terminal','windowTitel'))
except:
    window.title("Zeitenbuchungssystem")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(str(width) + "x" + str(height))
if read_config('Terminal','mouseCurserDeactivated') == 'True':
    window.config(cursor="none")
app = App(window)

log_level_dict = {'logging.DEBUG': logging.DEBUG, 
                        'logging.INFO': logging.INFO,
                        'logging.WARNING': logging.WARNING,
                        'logging.ERROR': logging.ERROR,
                 }

try:
    basedir = read_config('Terminal','logPath')
    logFile = f'{basedir}Terminal.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open(logFile, 'w+')
    logging.basicConfig(filename=logFile,level=log_level_dict.get(read_config('Terminal','logLevel'),logging.INFO),format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
rotate_handler = RotatingFileHandler(filename=logFile, maxBytes=10000000,backupCount=5)
logger.addHandler(rotate_handler)
logger.info('Starting Terminal')

try:
    logging.debug("Thats a debug message")
    logging.info("Thats an info message")
    logging.error("Thats an error message")
    request_token()
    init_local_failover_database()
    window.mainloop()
except KeyboardInterrupt():
    logger.warning('Quitting application, received keyboard interrupt')
    sys.exit(0)
except Exception as e:
    logger.error('Setting labels for Messages')
    pass
