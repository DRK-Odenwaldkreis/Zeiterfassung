#!/usr/bin/python3
# coding=utf-8
import os
import MySQLdb
import sys
import logging

logger = logging.getLogger('Database')
logger.debug('Logger for database was initialised')

from utils.readconfig import read_config

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
            self.connection = MySQLdb.connect(
                host=self.__host, user=self.__user, passwd=self.__passwd, db=self.__dbName)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error('The following error occured in constructor of database: %s' % (e))
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
        finally:
            self.cursor.close()

    def update(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logger.error(
                'The following error occured in updating: %s' % (e))
            self.connection.rollback()
            raise UpdateError
        finally:
            self.cursor.close()

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

    def read_single(self,query):
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
    test.read_single(query = sql)
