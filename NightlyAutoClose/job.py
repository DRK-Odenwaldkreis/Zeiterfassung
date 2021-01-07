#!/usr/bin/python3
# coding=utf-8
from os import path
import logging
import sys
from database import Database

logFile = 'rotationJob.log'
logging.basicConfig(filename=logFile, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Nightly Auto Clean')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Update Dienste SET Dienstende = current_timestamp(), AutoClosed = '1' WHERE Dienstende is NULL"
        logger.debug('Closing shift, using the following query: %s' % (sql))
        DatabaseConnect.update(sql)
    except Exception as e:
        logging.error("Error")