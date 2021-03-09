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
import sys
import logging
import datetime
sys.path.append("..")
from utils.database import Database

logger = logging.getLogger('Pausenberechnung')
logger.debug('Logger for pausen berechnung was initialised')


def calculate_net_shift_time(start,end):
    try:
        logging.debug("Calculation of brutto times with following start and end: Start: %s, End: %s" % (start,end))
        firstBreak = datetime.timedelta(minutes=0)
        secondBreak = datetime.timedelta(minutes=0)
        bruttoShiftTime = end - start
        logging.debug("Brutto shift times are calculated as: %s" % (bruttoShiftTime))
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
        logging.debug("Second break due to 9 hours is calculated as : %s" % (secondBreak))
        netShiftTime = bruttoShiftTime - firstBreak - secondBreak
        netShiftTimeHours = netShiftTime.seconds//3600
        netShiftTimeMinutes = (netShiftTime.seconds % 3600)//60
        totalBreakTime = firstBreak + secondBreak
        return netShiftTime, netShiftTimeHours, netShiftTimeMinutes, totalBreakTime
    except Exception as err:
        logging.debug("Raised exception within the net shift calculation with the following message: %s"% (err))
        return datetime.timedelta(hours=0,minutes=0), 0, 0

def calculate_net_shift_sum_time(entries):
    netShiftTimeSum = 0
    for i in entries:
        netShiftTime, netShiftTimeHours, netShiftTimeMinutes, totalBreakTime = calculate_net_shift_time(
            i[0], i[1])
        netShiftTimeSum = netShiftTimeSum + netShiftTime.seconds
    return round(netShiftTimeSum/3600,2)



