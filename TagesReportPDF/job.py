#!/usr/bin/python3
# coding=utf-8
from os import path
import logging
import sys
from database import Database
from pdfcreator.pdf import PDFgenerator

logFile = 'reportJob.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Daily Report')
logger.debug('Starting')

if __name__ == "__main__":
    #try:
        DatabaseConnect = Database()
        sql = "Select Dienste.Personalnummer, Dienste.Dienstbegin, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art, Dienste.AutoClosed FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer where Dienstbegin > (NOW() - INTERVAL 24 HOUR);"
        logger.debug('Getting all Events from Yesterday with the following query: %s' % (sql))
        content = DatabaseConnect.read_all(sql)
        #logger.debug('Received the following entries: %s' % (str(content)))
        PDF = PDFgenerator(content)
        PDF.generate()
    #except Exception as e:
    #    logging.error("Error")
