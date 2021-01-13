#!/usr/bin/python3
# coding=utf-8

import logging
import datetime


logFile = '../../Logs/pausen.log'
logging.basicConfig(filename=logFile, level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Pausenberechnung')
logger.debug('Logger for pausen berechnung was initialised')



def calculate_net_shift_time(start,end):
    logging.debug("Calculation of brutto times with following start and end: Start: %s, End: %s" % (start,end))
    firstBreak = datetime.timedelta(minutes=0)
    secondBreak = datetime.timedelta(minutes=0)
    bruttoShiftTime = end - start
    logging.debug("Brutto shitft times are calculated as: %s" % (bruttoShiftTime))
    bruttoShiftTimeHours = bruttoShiftTime.seconds//3600
    bruttoShiftTimeMinutes = (bruttoShiftTime.seconds % 3600)//60
    if bruttoShiftTimeHours == 6:
        firstBreak = datetime.timedelta(minutes=abs(bruttoShiftTimeMinutes - 0))
        if (firstBreak.seconds % 3600)//60 > 30:
            firstBreak = datetime.timedelta(minutes=30)
    elif bruttoShiftTimeHours >6:
        firstBreak = datetime.timedelta(minutes=30)
    logging.debug("First break due to 6 hours is calculated as : %s" % (firstBreak))
    if bruttoShiftTimeHours == 9:
        secondBreak = datetime.timedelta(
            minutes=abs(bruttoShiftTimeMinutes - 0))
        if (secondBreak.seconds % 3600)//60 > 15:
            secondBreak = datetime.timedelta(minutes=15)
    elif bruttoShiftTimeHours > 9:
        secondBreak = datetime.timedelta(minutes=15)
    logging.debug("Sceond break due to 9 hours is calculated as : %s" % (secondBreak))
    netShiftTime = bruttoShiftTime - firstBreak - secondBreak
    netShiftTimeHours = netShiftTime.seconds//3600
    netShiftTimeMinutes = (netShiftTime.seconds % 3600)//60
    return netShiftTime, netShiftTimeHours, netShiftTimeMinutes
