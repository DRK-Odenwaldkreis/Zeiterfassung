from zipfile import ZipFile
import sys
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator
from utils.month import monthInt_to_string
from utils.getRequesterMail import get_Mail_from_UserID
import datetime
import time
import logging


logFile = '../../Logs/planning.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Dienstplanung Report')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            logger.debug('Starting Planning creation')
        else:
            logger.debug(
                'Input parameters are not correct, Month and Year are needed')
            raise Exception
        logger.debug(
            'Was started for the following week: %s' % (sys.argv[1]))
        logger.debug(
            'Was started for the following year: %s' % (sys.argv[2]))
        requestedWeek = sys.argv[1]
        requestedYear = sys.argv[2]
        DatabaseConnect = Database()
        sql = "Select  Personal.Vorname, Personal.Nachname, Planung.Schicht, Planung.Datum, Planung.Comment FROM Planung JOIN Personal ON Personal.Personalnummer = Planung.Personalnummer where WEEK(Datum,5) = '%s' and YEAR(Datum) = '%s' order by Datum;" % (
            requestedWeek, requestedYear)
        logger.debug(
            'Getting all planning data with the following query: %s' % (sql))
        content = DatabaseConnect.read_all(sql)
        logger.debug('Received the following content: %s' % (str(content)))
        PDF = PDFgenerator(content, requestedWeek, requestedYear)
        PDF.generate()
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
