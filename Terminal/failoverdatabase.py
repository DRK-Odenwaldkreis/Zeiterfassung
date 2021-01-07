#!/usr/bin/python3
# coding=utf-8
import os
import sqlite3
import sys
import logging

logger = logging.getLogger('Failover in local DB')
logger.debug('Logger for failover database was initialised')

def create_backup_event(hash):
    try:
        logger.debug('Creating local copy of data from following hash: %s' % (hash))
        connection = sqlite3.connect("./Backup.db")
        cursor = connection.cursor()
        sql = """INSERT INTO Dienste ("Hash") Values (%s)"""%(hash)
        logger.debug(
            'Wiriting to database using the following query: %s' % (sql))
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.error(
            'The following error occured in create backup event, rolling back: %s' % (e))
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    create_backup_event(1234)
