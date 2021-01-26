from zipfile import ZipFile
import sys
sys.path.append("..")
from utils.database import Database
from pdfcreator.pdf import PDFgenerator
from utils.month import monthInt_to_string
from utils.sendmail import send_mail_download
from utils.getRequesterMail import get_Mail_from_UserID
import datetime
import time
import locale
import logging


logFile = '../../Logs/singleReportJob.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Single Report')
logger.debug('Starting')

type = ""
latestFilename = ""
### TODO: 
# - Welches encoding genutzt wird muss in eine Config Datei
# - im pdfcreator: Wo die Schriftart liegt muss relativ angegeben werden - done


#locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

if __name__ == "__main__":
    try:
        if len(sys.argv) == 4:
            logger.debug(
                'Type is for all employee')
            type = "all"
        elif len(sys.argv) == 5:
            logger.debug(
                'Type is for single employee')
            requestedPersonalnummer = sys.argv[4]
            type = "single"
            logger.debug(
                'Was started for the following personalnummer: %s' % (sys.argv[4]))
        else:
            logger.debug(
                'Input parameters are not correct, Month and Year, requester and/or Personalnummer are needed')
            raise Exception
        logger.debug(
            'Was started for the following month: %s' % (sys.argv[1]))
        logger.debug(
            'Was started for the following year: %s' % (sys.argv[2]))
        requestedMonth = sys.argv[1]
        requestedYear = sys.argv[2]
        requester = sys.argv[3]
        DatabaseConnect = Database()
        if type == "single":
            sql = "SELECT Vorname,Nachname,Personalnummer FROM Personal WHERE Personalnummer = %s;" % (requestedPersonalnummer)
        else:
            sql = "SELECT Vorname,Nachname,Personalnummer FROM Personal where Aktiv=1;"
            zipFilename = '../../Reports/Einzelnachweise_' + monthInt_to_string(int(requestedMonth)) + '_' + requestedYear + '.zip'
            zipObj = ZipFile(zipFilename, 'w')
        logger.debug(
            'Getting employee infos with the following query: %s' % (sql))
        employee = DatabaseConnect.read_all(sql)
        logger.debug('Received the following employee: %s' % (str(employee)))
        for i in employee:
            vorname = i[0]
            nachname = i[1]
            personalnummer = i[2]
            sql = "SELECT Dienstbeginn, Dienstende, Art FROM Dienste WHERE Personalnummer = %s AND MONTH(Dienstbeginn)=%s AND YEAR(Dienstbeginn)=%s AND Dienstende IS NOT NULL ORDER BY Dienstbeginn ASC;" % (
                personalnummer, requestedMonth, requestedYear)
            logger.debug('Getting all Events for employee of the month with the following query: %s' % (sql))
            shiftTimes = DatabaseConnect.read_all(sql)
            logger.debug('Received the following entries: %s' % (str(shiftTimes)))
            PDF = PDFgenerator(shiftTimes, nachname, vorname, personalnummer, requestedMonth, requestedYear)
            singleFilename = PDF.generate()
            if type == "all":
                zipObj.write(singleFilename, singleFilename.replace('../../Reports/Einzelnachweis_', 'Einzelnachweise_'))
            latestFilename = singleFilename
        logger.debug('Done')
        if type == "single":
            print(latestFilename.replace('../../Reports/', ''))
        else:
            zipObj.close()
            send_mail_download(zipFilename.replace(
                '../../Reports/', ''), get_Mail_from_UserID(requester))
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
        print("Error")
