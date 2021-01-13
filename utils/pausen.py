#!/usr/bin/python3
# coding=utf-8

import logging
import datetime

logger = logging.getLogger('Pausenberechnung')
logger.debug('Logger for pausen berechnung was initialised')


def calculate_net_shift_time(start,end):
    firstBreak = datetime.timedelta(minutes=0)
    secondBreak = datetime.timedelta(minutes=0)
    bruttoShiftTime = end - start
    bruttoShiftTimeHours = bruttoShiftTime.seconds//3600
    bruttoShiftTimeMinutes = (bruttoShiftTime.seconds % 3600)//60
    if bruttoShiftTimeHours == 6:
        firstBreak = datetime.timedelta(minutes=abs(bruttoShiftTimeMinutes - 0))
        if (firstBreak.seconds % 3600)//60 > 30:
            firstBreak = datetime.timedelta(minutes=30)
    elif bruttoShiftTimeHours >6:
        firstBreak = datetime.timedelta(minutes=30)
    if bruttoShiftTimeHours == 9:
        secondBreak = datetime.timedelta(
            minutes=abs(bruttoShiftTimeMinutes - 0))
        if (secondBreak.seconds % 3600)//60 > 15:
            secondBreak = datetime.timedelta(minutes=15)
    elif bruttoShiftTimeHours > 9:
        secondBreak = datetime.timedelta(minutes=15)
    netShiftTime = bruttoShiftTime - firstBreak - secondBreak
    netShiftTimeHours = netShiftTime.seconds//3600
    netShiftTimeMinutes = (netShiftTime.seconds % 3600)//60
    return netShiftTime, netShiftTimeHours, netShiftTimeMinutes
