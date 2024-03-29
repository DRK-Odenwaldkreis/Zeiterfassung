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

import sys
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_mail_new_dienstplan
from utils.getRequesterMail import get_Mail_from_UserID
import logging


logFile = '../../Logs/dienstplan.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('New Dienstplan')
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
        plannedWeek = sys.argv[1]
        plannedYear = sys.argv[2]
        DatabaseConnect = Database()
        sql = "Select id_li_user FROM Personal WHERE Aktiv=1 and id_li_user group by id_li_user;"
        allActivePeople = []
        for i in DatabaseConnect.read_all(sql):
            allActivePeople.append(i[0])
        logger.debug('Received the following content: %s' %(str(allActivePeople)))
        mailList = []
        for i in allActivePeople:
            mailList.append(get_Mail_from_UserID(i))
        logger.debug('Created the following mailing list: %s' % (mailList))
        send_mail_new_dienstplan(mailList, plannedWeek, plannedYear)
    except Exception as e:
       logging.error("The following error occured in reminder job: %s" % (e))
       print("Error")
    finally:
        DatabaseConnect.close_connection()
