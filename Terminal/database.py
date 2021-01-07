#!/usr/bin/python3
# coding=utf-8
import os
import MySQLdb
import sys


from readconfig import read_config

class Disconntect(Exception):
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
            self.__host = read_config("MariaDB", "host")
            self.__user = read_config("MariaDB", "user")
            self.__passwd = read_config("MariaDB", "pw")
            self.__dbName = read_config("MariaDB", "db")
            self.connection = MySQLdb.connect(
                host=self.__host, user=self.__user, passwd=self.__passwd, db=self.__dbName)
            self.cursor = self.connection.cursor()
        except Exception as err:
            print(err)

#Insert,Update, read_all and read_single
    def insert(self, query, tupel):
        try:
            self.cursor.execute(query, tupel)
        except:
            raise InsertError
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
            raise UpdateError
        finally:
            self.cursor.close()

    def update(self, query):
        try:
            self.cursor.execute(query)
        except:
            raise UpdateError
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
            raise InsertError
        finally:
            self.cursor.close()

    def read_all(self, query):
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
        except:
            raise QueryError
        if self.result is not None:
            return self.result
        else:
            pass

    def read_single(self,query):
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchone()
        except:
            raise QueryError
        if self.result is not None:
            return self.result
        else:
            pass


if __name__ == "__main__":
    test = Database()
    sql = 'Select * from Personal'
    test.read_single(query = sql)
