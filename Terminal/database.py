#!/usr/bin/python3
# coding=utf-8
import os
import glob
import MySQLdb
import time
import math
import sys


from readconfig import read_config

class Disconntect(Exception):
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
        self.cursor.execute(query, tupel)
        try:
            self.connection.commit()
        except:
            self.connection.rollback()

    def update(self, query):
        self.cursor.execute(query)
        try:
            self.connection.commit()
        except:
            self.connection.rollback()

    def read_all(self, query):
        self.cursor.execute(query)
        self.result = self.cursor.fetchall()
        if self.result is not None:
            return self.result
        else:
            pass

    def read_single(self,query):
        self.cursor.execute(query)
        self.result = self.cursor.fetchone()
        if self.result is not None:
            return self.result
        else:
            pass


if __name__ == "__main__":
    test = Database()
    sql = 'Select * from Personal'
    test.read_single(query = sql)
