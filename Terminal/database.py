#!/usr/bin/python3
# coding=utf-8
import os
import mysql.connector
import sys
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
            self.__host= '10.0.1.8'
            self.__user= 'root123'
            self.__passwd = 'Test1234'
            self.__dbName = 'Impfzentrum'
            self.connection = mysql.connector.connect(
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
    print(test.read_single(query = sql))
