#!/usr/bin/python3
# coding=utf-8
import os
import sqlite3
import sys

def create_backup_event(hash):
    try:
        connection = sqlite3.connect("./Backup.db")
        cursor = connection.cursor()
        sql = """INSERT INTO Dienste ("Hash") Values (%s)"""%(hash)
        cursor.execute(sql)
        connection.commit()
    except Error as e:
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    create_backup_event(1234)
