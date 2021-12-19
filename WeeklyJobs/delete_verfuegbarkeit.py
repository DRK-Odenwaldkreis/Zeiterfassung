#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Zeiterfassung.

from os import path,makedirs
import logging
import sys
sys.path.append("..")
from utils.database import Database
import datetime

try:
    basedir = '../../Logs/'
    logFile = f'{basedir}clean.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open(logFile, 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Deleting planning data started on: {datetime.datetime.now()}')
logger.info('Starting')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Delete from Planung WHERE Datum <= (NOW() - INTERVAL 42 DAY);"
        logger.debug(f'Cleaning all Planungsentries that are older than 42 days, using the following query: {sql}')
        DatabaseConnect.delete(sql)
        logger.info('Done')
    except Exception as e:
        logger.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured in loop for unverified: {e}')
