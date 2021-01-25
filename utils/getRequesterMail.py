#!/usr/bin/python3
# coding=utf-8
import os
import sys
sys.path.append("..")
from utils.database import Database

def get_Mail_from_UserID(id):
    try:
        DatabaseConnect = Database()
        sql = 'Select username from li_user where id = %s' % (id)
        userMail = DatabaseConnect.read_single(sql)
        return userMail[0]
    except:
        return "service@impfzentrum-odw.de"
