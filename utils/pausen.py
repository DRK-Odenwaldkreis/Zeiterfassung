#!/usr/bin/python3
# coding=utf-8

import logging

logger = logging.getLogger('Pausenberechnung')
logger.debug('Logger for pausen berechnung was initialised')

def calculate_net_shift_time(start,end):
    netShiftTime = end - start
    netShiftTimeHours = netShiftTime.seconds//3600
    netShiftTimeMinutes = (netShiftTime.seconds % 3600)//60
    return netShiftTime, netShiftTimeHours, netShiftTimeMinutes
