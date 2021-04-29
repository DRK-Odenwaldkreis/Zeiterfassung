#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import csv
import logging

from datetime import datetime
from datetime import timedelta
sys.path.append("..")
from utils.pausen import calculate_net_shift_time
from utils.lohnart import get_lohnart

netShiftTime=0
netShiftTimeHours=0
netShiftTimeMinutes=0

logger = logging.getLogger('CSV Export')
logger.debug('Logger for createCSV was initialised')

def create_row(entry,lohnart,month):
    netShiftTime, netShiftTimeHours, netShiftTimeMinutes, breakTimes = calculate_net_shift_time(entry[1], entry[2])
    if not entry[7]:
        logger.debug("Stundensatz not set, setting to xx,yy")
        stundensatz="xx,yy"
    else:
        logger.debug("Stundensatz is set to %s: " % entry[7])
        stundensatz=entry[7]
    try:
        if entry[0] < 6000:
            logger.debug("In entry[0] <= 6000")
            return False
        elif entry[6] == 1 and lohnart == 490:
            logger.debug("In entry[6]== 1 and lohnart == 490")
            return False
        elif entry[6] == 1 and lohnart == 566:
            logger.debug("In entry[6]== 1 and lohnart == 566")
            return False
        elif entry[6] == 1 and lohnart == 567:
            logger.debug("In entry[6]== 1 and lohnart == 567")
            return False
        elif lohnart == 555:
            logger.debug("Lohnart == 555")
            date = entry[2].replace(hour=21,minute=0,second=0)
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round((entry[2]-date).seconds/3600, 2)).replace(".", ","), str(stundensatz), "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 1 and lohnart == 558:
            logger.debug("In entry[6]== 1 and lohnart == 558")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(stundensatz), "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 1 and lohnart == 556:
            logger.debug("In entry[6]== 1 and lohnart == 556")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(stundensatz), "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 0 and lohnart == 490:
            logger.debug("In entry[6]== 0 and lohnart == 490")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 0 and lohnart == 558:
            logger.debug("In entry[6]== 0 and lohnart == 558")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(stundensatz), "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 0 and lohnart == 556:
            logger.debug("In entry[6]== 0 and lohnart == 556")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(stundensatz), "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 0 and lohnart == 567:
            logger.debug("In entry[6]== 0 and lohnart == 567")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        elif entry[6] == 0 and lohnart == 566:
            logger.debug("In entry[6]== 0 and lohnart == 566")
            return ["[VARTAB]", "INSERT", "800", "4", entry[0], entry[4], entry[3], "1", lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", entry[1].replace(day=1).strftime("%Y-%m-%d"), entry[1].replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", entry[1].replace(day=1).strftime("%Y-%m-%d")]
        else:
            logger.debug("In else, did not find a matching value")
            return False
    except Exception as e:
        logger.debug("The following error occured: %s" %(e))


def create_CSV(content, month, year):
    filename = "../../Reports/CSVExport_" + str(month) + "_" + str(year) + ".csv"
    errorFilename = "../../Reports/CSVExport_OUTLINER_"+ str(month) + "_" + str(year) + ".csv"
    with open(errorFilename, mode='w', newline='') as errorfile:
        writeErrorEntry = csv.writer(errorfile,delimiter=';')
        writeErrorEntry.writerow(["Personalnummer","Begin","Ende","Dauer","Name","Vorname","Dienstart"])
        with open(filename, mode='w', newline='') as csvfile:
            writeEntry = csv.writer(csvfile, delimiter=';')
            writeEntry.writerow(["Satzart", 
                                "Funktion",
                                "MAN",
                                "AK",
                                "PNR",
                                "Name",
                                "Vorname",
                                "VERTNR",
                                "LA",
                                "VD_ETAGE",
                                "VD_ESTD",
                                "VD_EFAKT",
                                "VD_EBETRAG",
                                "KST",
                                "KOSTART",
                                "VD_KTR",
                                "VD_DAT",
                                "VD_ZDAT",
                                "VD_HER",
                                "VD_HER_DAT"
                                ])
            for i in content:
                netShiftTime, netShiftTimeHours, netShiftTimeMinutes, breakTimes = calculate_net_shift_time(i[1],i[2])
                lohnart = get_lohnart(i[1],i[5],i[2])
                for z in lohnart:
                    new_entry = create_row(i, z, month)
                    if new_entry:
                        writeEntry.writerow(new_entry)
                    else:
                        writeErrorEntry.writerow([i[0], i[1], i[2], str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), i[3], i[4], i[5]])
    return filename, errorFilename


def create_sum_CSV(content,month,year):
    filename = "../../Reports/CSVExport_SUMMENUEBERSICHT_" + str(month) + "_" + str(year) + ".csv"
    with open(filename, mode='w', newline='') as file:
        writeEntry = csv.writer(file, delimiter=';')
        writeEntry.writerow(["Personalnummer", "Summe"])
        for key, value in content.items():
            writeEntry.writerow([key,str(value).replace(".",",")])
        return filename


