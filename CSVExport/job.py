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


import logging
import locale
import time
import datetime
from zipfile import ZipFile
import sys
sys.path.append("..")
from utils.database import Database
from utils.pausen import calculate_net_shift_sum_time
from utils.month import monthInt_to_string
from utils.sendmail import send_mail_csvexport_download
from utils.getRequesterMail import get_Mail_from_UserID
from createCSV import create_CSV
from createCSV import create_sum_CSV

logFile = '../../Logs/CSVExportJob.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CSV Export')
logger.debug('Starting')


if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            logger.debug(
                'Input parameters are not correct, Month, Year and requester needed')
            raise Exception
        logger.debug(
            'Was started for the following month: %s' % (sys.argv[1]))
        logger.debug(
            'Was started for the following year: %s' % (sys.argv[2]))
        logger.debug(
            'Was started for the following requester: %s' % (sys.argv[3]))
        requestedMonth = sys.argv[1]
        requestedYear = sys.argv[2]
        requester = sys.argv[3]
        DatabaseConnect = Database()
        sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Personal.Hauptamtlich, Lohngruppe.Stundensatz, Lohngruppe.SFN, Personal.AK, Personal.VTNR, Personal.MAN FROM Dienste as Dienste JOIN Personal as Personal ON Personal.Personalnummer = Dienste.Personalnummer LEFT JOIN Lohngruppe ON Personal.Gruppe = Lohngruppe.Bezeichnung WHERE MONTH(Dienste.Dienstbeginn)=%s AND YEAR(Dienste.Dienstbeginn)= %s AND Dienste.Dienstende is not Null AND Personal.Aktiv = 1 ORDER BY Dienste.Dienstbeginn ASC;" % (
            requestedMonth, requestedYear)
        logger.debug('Getting all Events for employee of the month and year with the following query: %s' % (sql))
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' %
                     (str(exportEvents)))
        filename,errorFilename = create_CSV(exportEvents, requestedMonth, requestedYear)
        logger.debug('Done')
        sql = "SELECT Dienste.Personalnummer FROM Dienste as Dienste JOIN Personal as Personal ON Personal.Personalnummer = Dienste.Personalnummer WHERE MONTH(Dienste.Dienstbeginn)=%s and YEAR(Dienste.Dienstbeginn)=%s and Personal.Hauptamtlich=0"%(requestedMonth,requestedYear)
        personalnummer = DatabaseConnect.read_all(sql)
        personalNetShiftSums = {}
        for i in personalnummer:
            sum = 0
            sql = "SELECT Dienstbeginn, Dienstende FROM Dienste WHERE Personalnummer = %s AND MONTH(Dienstbeginn)=%s AND YEAR(Dienstbeginn)=%s AND Dienstende is not NULL ORDER BY Dienstbeginn ASC;" % (
                i[0], requestedMonth, requestedYear)
            DatabaseConnect.read_all(sql)
            sum = calculate_net_shift_sum_time(DatabaseConnect.read_all(sql))
            personalNetShiftSums[i[0]] = sum
        sumFilename = create_sum_CSV(
            personalNetShiftSums, requestedMonth, requestedYear)
        zipFilename = '../../Reports/CSVExport_' + monthInt_to_string(int(requestedMonth)) + '_' + requestedYear + '.zip'
        zipObj = ZipFile(zipFilename, 'w')
        zipObj.write(filename, filename.replace('../../Reports/', ''))
        zipObj.write(errorFilename, errorFilename.replace('../../Reports/', ''))
        zipObj.write(sumFilename, sumFilename.replace('../../Reports/', ''))
        zipObj.close()
        send_mail_csvexport_download(zipFilename.replace('../../Reports/', ''), get_Mail_from_UserID(requester))
        print(zipFilename)
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
    finally:
        DatabaseConnect.close_connection()
