#!/usr/bin/python3
# coding=utf-8
import os
import glob
import time
import math
import sys
import datetime

from database import Database

class PersonUnknown(Exception):
    pass

class QRInvalid(Exception):
    pass

class DeadTime(Exception):
    pass

class UnknownState(Exception):
    pass

class UnableToWrite(Exception):
    pass

class ScanEvent(object):

    # Constructor
    def __init__(self,hash):
        try:
            self.hash = hash
            self.DatabaseConnect = Database()
        except Exception as e:
            print(e)

    def check_validity(self):
        if len(self.hash) != 4:
            raise QRInvalid

    def get_personal_number(self):
        self.sql = "Select Personalnummer, Vorname, Nachname from Personal where Hash=%s;" % (
            self.hash)
        self.identity = self.DatabaseConnect.read_single(self.sql)
        if self.identity == None:
            raise PersonUnknown
        self.personalnummer = self.identity[0]
        self.vorname = self.identity[1]
        self.nachname = self.identity[2]
    
    def check_dead_time(self):
        self.sql = "Select * from Dienste where Personalnummer=%s and Updated > (NOW() - INTERVAL 5 SECOND);" % (
            self.personalnummer)
        if self.DatabaseConnect.read_single(self.sql) != None:
            raise DeadTime


    def check_open_entries(self):
        self.sql = "Select * from Dienste where Personalnummer=%s and Dienstende is NULL" % (self.personalnummer)
        self.openEntries = self.DatabaseConnect.read_all(self.sql)
        if len(self.openEntries) == 0:
            self.direction = "Dienstbegin"
        elif len(self.openEntries) == 1:
            self.direction = "Dienstende"
            self.startTime = self.openEntries[0][2]
        else:
            raise UnknownState

    def create_shift(self):
        try:
            self.sql = "Insert into Dienste (Personalnummer) VALUES ('%s')"
            self.tupel = (self.personalnummer,)
            self.DatabaseConnect.insert(self.sql, self.tupel)
        except:
            raise UnableToWrite

    def close_shift(self):
        try:
            self.sql = "Update Dienste SET Dienstende = current_timestamp() WHERE Personalnummer = %s and Dienstende is NULL ORDER BY Dienstbegin DESC LIMIT 1" % (self.personalnummer)
            self.DatabaseConnect.update(self.sql)
        except:
            raise UnableToWrite
        finally:
            self.calc_shift()
            
    def calc_shift(self):
        try:
            self.shiftDuration = (datetime.datetime.now() - self.startTime)
            self.shiftDurationHours = (self.shiftDuration.seconds//3600)
            if self.shiftDurationHours < 10:
                self.shiftDurationHours = '0%s' % int(self.shiftDurationHours)
            else:
                self.shiftDurationHours = '%s' % int(self.shiftDurationHours)
            self.shiftDurationMinutes = (self.shiftDuration.seconds % 3600)//60
            if self.shiftDurationMinutes < 10:
                self.shiftDurationMinutes = '0%s' % int(self.shiftDurationMinutes)
            else:
                self.shiftDurationMinutes = '%s' % int(self.shiftDurationMinutes)
        except:
            self.shiftDurationHours = '00'
            self.shiftDurationMinutes = '00'



