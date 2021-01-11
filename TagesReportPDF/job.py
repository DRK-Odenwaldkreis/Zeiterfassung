#!/usr/bin/python3
# coding=utf-8
from os import path
import logging
import sys
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator

logFile = '../Logs/reportJob.log'
logging.basicConfig(filename = logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Daily Report')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Select Dienste.Personalnummer, Dienste.Dienstbegin, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer where Dienstende is not Null AND Dienstbegin > (NOW() - INTERVAL 24 HOUR);"
        logger.debug('Getting all Events from Yesterday with the following query: %s' % (sql))
        content = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' % (str(content)))
        PDF = PDFgenerator(content)
        result = PDF.generate()
        sys.exit(result)
        logger.debug('Done')
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        sys.exit("Error")
