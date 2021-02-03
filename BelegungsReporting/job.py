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
import time
import datetime
import sys
sys.path.append("..")
from utils.database import Database

logFile = '../../Logs/rotationJob.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Besetzung Reporting')
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