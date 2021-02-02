import sys
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_mail_reminder
from utils.getRequesterMail import get_Mail_from_UserID
from utils.getRequesterMail import get_Mail_List
import datetime
import time
import logging
import os


logFile = '../../Logs/reminderPlanning.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Reminder Planning')
logger.debug('Starting')


if __name__ == "__main__":
    try:
        today = datetime.datetime.today()
        remindingWeek = int((today + datetime.timedelta(weeks=3)).strftime("%V"))
        remindingYear = int((today + datetime.timedelta(weeks=3)).strftime("%G"))
        logger.debug('Starting reminding for KW: %s and Year: %s' %(remindingWeek, remindingYear))
        DatabaseConnect = Database()
        sql = "Select  Personal.id_li_user FROM Planung JOIN Personal ON Personal.Personalnummer = Planung.Personalnummer where WEEK(Datum,5) = '%s' and YEAR(Datum) = '%s' and Personal.Aktiv=1 group by Personal.id_li_user;" % (
            remindingWeek, remindingYear)
        positiveFeedback = []
        for i in DatabaseConnect.read_all(sql):
            positiveFeedback.append(i[0])
        logger.debug(
            'Getting all people that entered feedback  with the following query: %s' % (sql))
        sql = "Select id_li_user FROM Personal WHERE Aktiv=1 and id_li_user group by id_li_user;" 
        allActivePeople = []
        for i in DatabaseConnect.read_all(sql):
            allActivePeople.append(i[0])
        logger.debug('Received the following content: %s' %
                     (str(allActivePeople)))
        list_difference = [
            item for item in allActivePeople if item not in positiveFeedback]
        logger.debug('Following staff id´s did not participate in planning: %s' %
                     (str(list_difference)))
        mailList = get_Mail_List(list_difference)
        logger.debug('Created the following mailing list: %s' % (mailList))
        logger.debug('Informing %s number of people of total %s active.' % (len(mailList), len(allActivePeople)))
        send_mail_reminder(mailList, remindingWeek, remindingYear)
    except Exception as e:
       logging.error("The following error occured in reminder job: %s" % (e))
       print("Error")
