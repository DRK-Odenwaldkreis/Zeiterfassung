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


def get_Mail_List(idList):
    try:
        DatabaseConnect = Database()
        sql = "Select username from li_user where id in %s" % (str(tuple(idList)))
        userMail = DatabaseConnect.read_all(sql)
        mailingList = []
        for i in userMail:
            mailingList.append(i[0])
        return mailingList
    except Exception as e:
        print("The following error occured in reminder job: %s" % (e))
