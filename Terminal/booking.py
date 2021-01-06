#!/usr/bin/python3
# coding=utf-8
import os
import glob
import pymysql
import time
import math
import sys

from database import Database

class PersonUnknown(Exception):
    pass

class QRInvalid(Exception):
    pass

class DeadTime(Exception):
    pass

class UnknownState(Exception):
    pass

class ScanEvent(object):

    # Constructor
    def __init__(self,hash):
        try:
            self.hash = hash
            self.DatabaseConnect = Database
        except Exception as e:
            print(e)

    def check_validity(self):
        print("In validation")
        if len(self.hash) != 4:
            raise QRInvalid

    def get_personal_number(self):
        print("Checking Number")
        self.identiy = self.DatabaseConnect.read_single(self,
            "Select Personalnummer,Vorname from Personal where Hash=%s;"%(self.hash))
        if len(self.identiy) == 0:
            raise PersonUnknown
        self.vorname = self.identiy[vorname]
        self.personalnummer = self.identity[personalnummer]
    
    def check_dead_time(self):
        if len(self.DatabaseConnect.read_single("Select * from Dienste where Personalnummer=%s and Updated > (NOW() - INTERVAL 10 SECONDS);") % (self.personalnummer)) > 0:
            raise DeadTime

    def check_open_entries(self):
        self.openEntries = self.DatabaseConnect.read_single(
            "Select * from Dienste where Personalnummer=%s and Dienstende is NULL") % (self.personalnummer)
        if len(self.openEntries) == 0:
            self.direction = "Dienstbeginn"
        elif len(self.openEntries) == 1:
            self.direction = "Dienstende"
        else:
            raise UnknownState

    def create_shift(self):
        self.DatabaseConnect.insert()

    def close_shift(self):
        self.DatabaseConnect.update()
        self.sum = get_sum()
    
    def get_sum(self):
        pass
