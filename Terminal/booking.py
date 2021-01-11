#!/usr/bin/python3
# coding=utf-8
import os
import glob
import time
import math
import sys
import datetime
import logging
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

class UnknownError(Exception):
    pass

class DatabaseDisconnect(Exception):
    pass

logger = logging.getLogger('ScanEvent')
logger.debug('Logger for ScanEvent was initialised')

class ScanEvent(object):

    # Constructor
    def __init__(self,hash):
        try:
            logger.debug('Constructor was called')
            self.hash = hash
            logger.debug('The following Hash was scanned: %s'%(self.hash))
            logger.debug('Starting Databaseconnect')
            self.DatabaseConnect = Database()
        except Exception as e:
            logger.error('The following error occured in the constructor such that DatabaseDisconnect exception will be raised: %s'%(e))
            raise DatabaseDisconnect
    #Currently hash is only 4 characters long, for dev
    def check_validity(self):
        logger.debug('Checking if QR is valid')
        if len(self.hash) != 8:
            logger.warning('The QR is not a valid QR Code')
            raise QRInvalid
        logger.debug('QR is valid')

    def get_personal_number(self):
        self.sql = "Select Personalnummer, Vorname, Nachname from Personal where Hash=%s;" % (
            self.hash)
        logger.debug(
            'Getting the Personalnummer and names, using the following query: %s'%(self.sql))
        self.identity = self.DatabaseConnect.read_single(self.sql)
        if self.identity == None:
            logger.warning('Person is unknown')
            raise PersonUnknown
        try:
            logger.debug('Person is known, received the following identity: %s' % (str(self.identity)))
            self.personalnummer = self.identity[0]
            self.vorname = self.identity[1]
            self.nachname = self.identity[2]
            logger.debug('Found the following Personalnummer, Vorname, Name in the identity: %s, %s, %s' % (
                self.personalnummer, self.vorname, self.nachname))
        except Exception as e:
            logger.error('The following error occured in get personal number: %s' % (e))
            raise UnknownError
        
    
    def check_dead_time(self):
        self.sql = "Select * from Dienste where Personalnummer=%s and Updated > (NOW() - INTERVAL 5 SECOND);" % (self.personalnummer)
        logger.debug('Checking if same code was scanned the last 5 secondsusing the following query: %s'%(self.sql))
        if self.DatabaseConnect.read_single(self.sql) != None:
            logger.warning('Code was scanned in the last 5 seconds, dropping scan event.')
            raise DeadTime
        logger.debug('Code was not scanned within the last 5 seconds')


    def check_open_entries(self):
        try:
            self.sql = "Select * from Dienste where Personalnummer=%s and Dienstende is NULL" % (self.personalnummer)
            logger.debug(
                'Checking whether there are open entries, using the following query: %s' % (self.sql))
            self.openEntries = self.DatabaseConnect.read_all(self.sql)
            logger.debug(
                'Received the following entries: %s' % (str(self.openEntries)))
            if len(self.openEntries) == 0:
                logger.debug('No other entries found, seems to be Dienstbeginn')
                self.direction = "Dienstbeginn"
            elif len(self.openEntries) == 1:
                logger.debug('One entry found, seems to be Dienstende')
                self.direction = "Dienstende"
                self.startTime = self.openEntries[0][2]
                logger.debug('Found shift start at: %s'%(self.startTime))
                self.AutoClosed = 0
            else:
                logger.debug('More than one entry found, seems to be Dienstende but marking it as AutoClosed')
                self.direction = "Dienstende"
                self.startTime = self.openEntries[0][2]
                logger.debug('Found shift start at: %s' % (self.startTime))
                self.AutoClosed = 1
        except Exception as e:
            logger.error('The following error occured in check open entries: %s' % (e))
            raise UnknownState

    def create_shift(self):
        try:
            self.sql = "Insert into Dienste (Personalnummer) VALUES ('%s')"
            self.tupel = (self.personalnummer,)
            logger.debug('Opening shift, using the following query and tupel: %s, %s' % (self.sql, self.tupel))
            self.DatabaseConnect.insert(self.sql, self.tupel)
        except Exception as e:
            logger.error('The following error occured, could not write: %s' % (e))
            raise UnableToWrite

    def close_shift(self):
        try:
            self.sql = "Update Dienste SET Dienstende = current_timestamp(), AutoClosed = '%s' WHERE Personalnummer = %s and Dienstende is NULL ORDER BY Dienstbeginn DESC LIMIT 1" % (self.AutoClosed, self.personalnummer)
            logger.debug(
                'Closing shift, using the following query: %s' % (self.sql))
            self.DatabaseConnect.update(self.sql)
        except Exception as e:
            logger.error(
                'The following error occured in close shift, could not write due to : %s' % (e))
            raise UnableToWrite
        finally:
            self.calc_shift()
            
    def calc_shift(self):
        try:
            logger.debug('Calculating sum of the shift')
            self.shiftDuration = (datetime.datetime.now() - self.startTime)
            self.shiftDurationHours = (self.shiftDuration.seconds//3600)
            #In order to have double digit hours and minutes checking whether minutes or hours is < 10.
            if self.shiftDurationHours < 10:
                self.shiftDurationHours = '0%s' % int(self.shiftDurationHours)
            else:
                self.shiftDurationHours = '%s' % int(self.shiftDurationHours)
            self.shiftDurationMinutes = (self.shiftDuration.seconds % 3600)//60
            if self.shiftDurationMinutes < 10:
                self.shiftDurationMinutes = '0%s' % int(self.shiftDurationMinutes)
            else:
                self.shiftDurationMinutes = '%s' % int(self.shiftDurationMinutes)
            logger.debug('Shift sum is %s hours and %s minutes' %(self.shiftDurationHours,self.shiftDurationMinutes))
        except Exception as e:
            logger.error('The following error occured, setting times to display to 00: %s' % (e))
            self.shiftDurationHours = '00'
            self.shiftDurationMinutes = '00'



