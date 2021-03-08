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
import sys
sys.path.append("..")
from utils.database import Database
from createCSV import create_CSV

logFile = '../../Logs/CSVExportJob.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CSV Export')
logger.debug('Starting')


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            logger.debug(
                'Input parameters are not correct, Month and Year needed')
            raise Exception
        logger.debug(
            'Was started for the following month: %s' % (sys.argv[1]))
        requestedMonth = sys.argv[1]
        requestedYear = sys.argv[2]
        DatabaseConnect = Database()
        sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Personal.Hauptamtlich, Lohngruppe.Stundensatz FROM Dienste as Dienste JOIN Personal as Personal ON Personal.Personalnummer = Dienste.Personalnummer LEFT JOIN Lohngruppe ON Personal.Gruppe = Lohngruppe.Bezeichnung WHERE MONTH(Dienste.Dienstbeginn)=%s AND YEAR(Dienste.Dienstbeginn)= %s AND Dienste.Dienstende is not Null AND Personal.Aktiv = 1 ORDER BY Dienste.Dienstbeginn ASC;" % (
            requestedMonth, requestedYear)
        logger.debug('Getting all Events for employee of the month and year with the following query: %s' % (sql))
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' %
                     (str(exportEvents)))
        filename = create_CSV(exportEvents, requestedMonth, requestedYear)
        logger.debug('Done')
        print(filename.replace('../../Reports', ''))
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
