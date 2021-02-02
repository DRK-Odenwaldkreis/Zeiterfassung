import logging
import time
import datetime
import sys
sys.path.append("..")
from utils.database import Database

logFile = '../../Logs/rotationJob.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Reminder Planning')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        logger.debug('Starting Belegungsreporting')
        DatabaseConnect = Database()
        sql = "SELECT COUNT(Dienste.Personalnummer) as Belegung FROM Dienste WHERE Day(Dienstbeginn)=day(now()) and Dienste.Dienstende is NULL and Dienste.Art='Normal';"
        count = DatabaseConnect.read_single(sql)[0]
        logger.debug('Getting current count of staff with the following query: %s' % (sql))
        logger.debug('Received the following count: %s' % (count))
        hour = datetime.datetime.now().hour
        logger.debug('Current hour used is: %s' % (hour))
        sql = "Insert into Besetzung (Stunde, Anzahl) VALUES ('%s', '%s')"
        logger.debug('Writing current statistics into Besetzung with the following query: %s' % (sql))
        tupel = (hour, count)
        DatabaseConnect.insert(sql, tupel)
    except Exception as e:
       logging.error("The following error occured in Belegungsreporting: %s" % (e))
       print("Error")