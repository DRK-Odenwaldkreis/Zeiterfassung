import sys
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator
import datetime
import time
import locale
import logging


logFile = '../Logs/singleReportJob.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Single Report')
logger.debug('Starting')

### TODO: 
# - Welches encoding genutzt wird muss in eine Config Datei
# - im pdfcreator: Wo die Schriftart liegt muss relativ angegeben werden - done


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            logger.debug('Input parameters are not correct, Personalnummer and Month and Year needed')
            raise Exception
        logger.debug(
            'Was started for the following personalnummer: %s' % (sys.argv[1]))
        logger.debug(
            'Was started for the following month: %s' % (sys.argv[2]))
        logger.debug(
            'Was started for the following year: %s' % (sys.argv[3]))
        requestedPersonalnummer = sys.argv[1]
        requestedMonth = sys.argv[2]
        requestedYear = sys.argv[3]
        
        DatabaseConnect = Database()

        sql = "SELECT Dienstbegin, Dienstende, Art FROM Dienste WHERE Personalnummer = %s AND MONTH(Dienstbegin)=%s AND YEAR(Dienstbegin)=%s AND Dienstende IS NOT NULL;" % (requestedPersonalnummer,requestedMonth,requestedYear)
        logger.debug('Getting all Events for employee of the month with the following query: %s' % (sql))
        shiftTimes = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' % (str(shiftTimes)))

        sql = "SELECT Vorname,Nachname FROM Personal WHERE Personalnummer = %s;" % (requestedPersonalnummer)
        logger.debug(
            'Getting employee infos with the following query: %s' % (sql))
        employee = DatabaseConnect.read_single(sql)
        logger.debug('Received the following employee: %s' % (str(employee)))
        vorname = employee[0]
        nachname = employee[1]
        PDF = PDFgenerator(shiftTimes, nachname, vorname, requestedPersonalnummer, requestedMonth, requestedYear)
        PDF.generate()
        logger.debug('Done')
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
