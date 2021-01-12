#!/usr/bin/python3
# coding=utf-8
from os import path
import logging
import sys
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator
from utils.sendmail import send_mail_report

logFile = '../../Logs/reportJob.log'
logging.basicConfig(filename = logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Daily Report')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        requestedMonth = sys.argv[1]
        requestedYear = sys.argv[2]
        if len(sys.argv) == 3:
            sql = sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer WHERE MONTH(Dienstbeginn)=%s AND YEAR(Dienstbeginn)=%s AND Dienstende IS NOT NULL ORDER BY Dienste.Dienstbeginn ASC;" % (
                requestedMonth, requestedYear)
        else:
            sql = "Select Dienste.Personalnummer, Dienste.Dienstbeginn, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer where Dienstende is not Null AND Dienstbeginn > (NOW() - INTERVAL 24 HOUR) ORDER BY Dienstbeginn ASC;"
        logger.debug('Getting all Events from Yesterday with the following query: %s' % (sql))
        content = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' % (str(content)))
        PDF = PDFgenerator(content)
        result = PDF.generate()
        logger.debug('Done')
        #send_mail_report()
        print(result)
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
