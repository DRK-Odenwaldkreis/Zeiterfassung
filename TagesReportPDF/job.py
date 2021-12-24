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

from os import path
import logging
import sys
import datetime
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator
from utils.sendmail import send_mail_report
from utils.getRequesterMail import get_Mail_from_UserID

logFile = '../../Logs/reportJob.log'
logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Daily Report')
logger.debug('Starting')
dailyReport = False

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        logger.debug(len(sys.argv))
        if len(sys.argv) == 3:
            requestedDate = sys.argv[1]
            requestedAK = sys.argv[2]
            sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer WHERE Date(Dienste.Dienstbeginn)='%s' AND Dienstende IS NOT NULL AND Personal.Abrechnungskreis = %s ORDER BY Dienste.Dienstbeginn ASC;" % (requestedDate, requestedAK)
        elif len(sys.argv) == 4:
            requestedAK = sys.argv[2]
            dailyReport = True
            requestedDate = datetime.datetime.now().strftime("%Y-%m-%d")
            sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed, Personal.Mandant FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer where Dienstende is not Null AND Personal.Abrechnungskreis = %s and Date(Dienstbeginn)=CURDATE() ORDER BY Dienstbeginn ASC;" % (requestedAK)
        logger.debug('Getting all Events from Yesterday with the following query: %s' % (sql))
        content = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' % (str(content)))
        PDF = PDFgenerator()
        PDF.start(content, requestedDate, requestedAK)
        result = PDF.generate()
        logger.debug('Done')
        if dailyReport:
            send_mail_report(result, datetime.datetime.now().date())
        print(result)
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
    finally:
        DatabaseConnect.close_connection()
