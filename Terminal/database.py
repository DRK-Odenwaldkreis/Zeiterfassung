#!/usr/bin/python3
# coding=utf-8
import os
import glob
import pymysql
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
            self.__dbPort = read_config("MariaDB", "port")
            self.connection = pymyqsl.connect(
                host=self.__host, user=self.__user, password=self.__passwd, database=self.__dbName, port=self.__dbPort)
            self.cursor = self.connection.cursor()
        except Exception as err:
            self.cursor.close()
            self.connection.close()
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
            return 0

    def read_single(self, query):
        self.cursor.execute(query)
        self.result = self.cursor.fetchone()
        if self.result is not None:
            return self.result
        else:
            return 0
