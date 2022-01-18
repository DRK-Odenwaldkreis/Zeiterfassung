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

import os
import sqlite3
import sys
import logging
from utils.readconfig import read_config

logger = logging.getLogger('Failover in local DB')
logger.debug('Logger for failover database was initialised')


def init_local_failover_database():
    filepath = read_config('LocalDB','filepath')
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS Dienste (id INTEGER,Hash	Char(64), Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(id AUTOINCREMENT));'''
    cursor.execute(sql)

def create_backup_event(hash):
    try:
        logger.debug('Creating local copy of data from following hash: %s' % (hash))
        connection = sqlite3.connect("./Backup.db")
        cursor = connection.cursor()
        sql = """INSERT INTO Dienste ("Hash") Values ('%s')"""%(hash)
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
