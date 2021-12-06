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

Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Personal.Hauptamtlich, Lohngruppe.Stundensatz, Lohngruppe.SFN, Personal.AK, Personal.VTNR, Personal.MAN

def create_row(entry,lohnart,month):
    personalNummer = int(entry[0])
    dienstBegin = entry[1]
    dienstEnde = entry[2]
    personalVorname = str(entry[3])
    personalNachname = str(entry[4])
    dienstArt = entry[5]
    dienstHauptamtlich = entry[6]
    lohnSatz = entry[7]
    lohnSFN = entry[8]
    personalAK = int(entry[9])
    personalVTNR = int(entry[10])
    personalMAN = int(entry[11])
    netShiftTime, netShiftTimeHours, netShiftTimeMinutes, breakTimes = calculate_net_shift_time(dienstBegin, dienstEnde)
    if not lohnSatz:
        logger.debug("Stundensatz not set, setting to xx,yy")
        stundensatz="xx,yy"
    else:
        logger.debug("Stundensatz is set to %s: " % lohnSatz)
        stundensatz=lohnSatz
    if not lohnSFN:
        logger.debug("Stundensatz not set, setting to xx,yy")
        sfn = "xx,yy"
    else:
        logger.debug("Stundensatz is set to %s: " % lohnSFN)
        sfn = lohnSFN
    try:
        if personalNummer < 6000:
            logger.debug("In personalNummer <= 6000")
            return False
        elif dienstHauptamtlich == 1 and lohnart == 490:
            logger.debug("In dienstHauptamtlich== 1 and lohnart == 490")
            return False
        elif dienstHauptamtlich == 1 and lohnart == 566:
            logger.debug("In dienstHauptamtlich== 1 and lohnart == 566")
            return False
        elif dienstHauptamtlich == 1 and lohnart == 567:
            logger.debug("In dienstHauptamtlich== 1 and lohnart == 567")
            return False
        elif lohnart == 555:
            logger.debug("Lohnart == 555")
            date = dienstEnde.replace(hour=21,minute=0,second=0)
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round((dienstEnde-date).seconds/3600, 2)).replace(".", ","), "", "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 1 and lohnart == 558:
            logger.debug("In dienstHauptamtlich== 1 and lohnart == 558")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(sfn), "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 1 and lohnart == 556:
            logger.debug("In dienstHauptamtlich== 1 and lohnart == 556")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(sfn), "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 0 and lohnart == 490:
            logger.debug("In dienstHauptamtlich== 0 and lohnart == 490")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 0 and lohnart == 558:
            logger.debug("In dienstHauptamtlich== 0 and lohnart == 558")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(sfn), "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 0 and lohnart == 556:
            logger.debug("In dienstHauptamtlich== 0 and lohnart == 556")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), str(sfn), "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 0 and lohnart == 567:
            logger.debug("In dienstHauptamtlich== 0 and lohnart == 567")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
        elif dienstHauptamtlich == 0 and lohnart == 566:
            logger.debug("In dienstHauptamtlich== 0 and lohnart == 566")
            return ["[VARTAB]", "INSERT", personalMAN, personalAK, personalNummer, personalNachname, personalVorname, personalVTNR, lohnart, "", str(round(netShiftTime.seconds/3600, 2)).replace(".", ","), "", "", "", "", "", dienstBegin.replace(day=1).strftime("%Y-%m-%d"), dienstBegin.replace(day=1).strftime("%Y-%m-%d"), "IMPVAR1", dienstBegin.replace(day=1).strftime("%Y-%m-%d")]
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


