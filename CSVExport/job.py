import logging
import locale
import time
import datetime


import sys
sys.path.append("..")

from utils.database import Database
from createCSV import create_CSV

logFile = '../Logs/CSVExportJob.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
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
        sql = "Select Dienste.Personalnummer, Dienste.Dienstbegin, Dienste.Dienstende, Personal.Vorname, Personal.Nachname, Dienste.Art FROM Dienste JOIN Personal ON Personal.Personalnummer = Dienste.Personalnummer WHERE MONTH(Dienstbegin)=%s AND YEAR(Dienstbegin)= %s AND Dienstende is not Null;" % (
            requestedMonth, requestedYear)
        logger.debug('Getting all Events for employee of the month and year with the following query: %s' % (sql))
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' %
                     (str(exportEvents)))
        filename = create_CSV(exportEvents, requestedMonth, requestedYear)
        logger.debug('Done')
        sys.exit(filename)
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
