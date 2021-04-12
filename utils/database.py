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
sys.path.append("..")
from utils.readconfig import read_config
import os
import mysql.connector
import logging

logger = logging.getLogger('Database')
logger.debug('Logger for database was initialised')


class Disconnect(Exception):
    pass


class InsertError(Exception):
    pass


class UpdateError(Exception):
    pass


class QueryError(Exception):
    pass


class Database(object):

    # Constructor
    def __init__(self):
        try:
            logger.debug('Constructor was called')
            self.__host = read_config("MariaDB", "host")
            self.__user = read_config("MariaDB", "user")
            self.__passwd = read_config("MariaDB", "pw")
            self.__dbName = read_config("MariaDB", "db")
            self.connection = mysql.connector.connect(
                host=self.__host, user=self.__user, passwd=self.__passwd, db=self.__dbName)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error(
                'The following error occured in constructor of database: %s' % (e))
            raise Disconnect

#Insert,Update, read_all and read_single
    def insert(self, query, tupel):
        try:
            self.cursor.execute(query, tupel)
            self.connection.commit()
        except Exception as e:
            logger.error(
                'The following error occured in inserting: %s' % (e))
            self.connection.rollback()
            raise UpdateError

    def update(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(
                'The following error occured in updating: %s' % (e))
            self.connection.rollback()
            raise UpdateError

    def read_all(self, query):
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
            if self.result is not None:
                return self.result
        except Exception as e:
            logger.error(
                'The following error occured in read all: %s' % (e))
            raise QueryError

    def read_single(self, query):
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchone()
            if self.result is not None:
                return self.result
        except Exception as e:
            logger.error(
                'The following error occured in read all: %s' % (e))
            raise QueryError


if __name__ == "__main__":
    test = Database()
    sql = 'Select * from Personal'
    print(test.read_single(query=sql))
