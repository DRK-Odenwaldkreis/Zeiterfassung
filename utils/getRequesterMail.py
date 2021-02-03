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
