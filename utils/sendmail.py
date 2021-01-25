#!/usr/bin/python3
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
import sys
sys.path.append("..")

from utils.readconfig import read_config

logger = logging.getLogger('Send Mail')
logger.debug('Starting')

FROM_EMAIL = read_config("Mail", "FROM_EMAIL")
TO_EMAIL = read_config("Mail", "TO_EMAIL")
SMTP_SERVER = read_config("Mail", "SMTP_SERVER")
SMTP_USERNAME = read_config("Mail", "SMTP_USERNAME")
SMTP_PASSWORD = read_config("Mail", "SMTP_PASSWORD")


def send_mail_report(filename, day, requester):
    try:
        logging.debug("Receviced the following filename %s to be sent to %s" % (filename, requester))
        message = MIMEMultipart()
        message.attach(MIMEText("Hallo,\n ein neuer Tagesreport wurde angelegt.",'plain'))
        message['Subject'] = "Neue Tagesreport für: %s" % (str(day))
        message['From'] = 'report@impfzentrum-odw.de'
        message['To'] = requester
        filenameRaw = filename
        filename = '../../Reports/' + str(filenameRaw)
        files = []
        files.append(filename)
        for item in files:
            attachment = open(item, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', "attachment; filename= " + item.replace('../../Reports/', ''))
            message.attach(part)
        smtp = smtplib.SMTP(SMTP_SERVER,port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(message['From'], message['To'], message.as_string())
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error(
            "The following error occured in send mail download: %s" % (err))
        return False


def send_mail_reminder(listRecipients, week, year):
    try:
        logging.debug("Receviced the following list of recipients: %s to be sent to." % (
            listRecipients))
        message = MIMEMultipart()
        message.attach(MIMEText("Hallo,\ndu hast für die KW %s in %s keine Planung abgegeben. \nDie Planung wird bald geschlossen. Bitte trage falls möglich noch deine Verfügbarkeiten ein. \n \nFalls du generelle nicht mehr unterstützen kannst, kannst du dich auch inaktiv schalten lassen." % (str(week), str(year)), 'plain'))
        message['Subject'] = "Erinnerung für Planung KW %s in %s" % (str(week), str(year))
        message['From'] = 'planung@impfzentrum-odw.de'
        message['Bcc'] = ", ".join(listRecipients)
        smtp = smtplib.SMTP(SMTP_SERVER, port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(message['From'], message['Bcc'], message.as_string())
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error(
            "The following error occured in send mail download: %s" % (err))
        return False


def send_mail_new_dienstplan(listRecipients, week, year):
    try:
        logging.debug("Receviced the following list of recipients: %s to be sent to." % (
            listRecipients))
        message = MIMEMultipart()
        message.attach(MIMEText("Hallo,\nes gibt für die KW %s in %s einen neuen Plan. \nDer Plan ist um Portal zu finden. \nFalls du generelle nicht mehr unterstützen kannst, kannst du dich auch inaktiv schalten lassen." % (str(week), str(year)), 'plain'))
        message['Subject'] = "Neue Planung für KW %s in %s" % (
            str(week), str(year))
        message['From'] = 'dienstplan@impfzentrum-odw.de'
        message['Bcc'] = ", ".join(listRecipients)
        smtp = smtplib.SMTP(SMTP_SERVER, port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(message['From'], message['Bcc'], message.as_string())
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error(
            "The following error occured in send mail download: %s" % (err))
        return False


def send_mail_download(filename, requester):
    try:
        logging.debug("Receviced the following filename %s to be sent to %s" % (filename, requester))
        message = MIMEMultipart()
        url = 'https://impfzentrum-odw.de/download.php?file=' +  str(filename)
        logging.debug("The created url is %s" % (url))
        message.attach(MIMEText("Hallo,\nEinzelnachweise wurden generiert und sind jetzt verfügbar.\nDiese können unter folgender URL heruntergeladen werden: %s" % (url), 'plain'))
        message['Subject'] = "Einzelnachweise sind zum Download verfügbar"
        message['From'] = 'report@impfzentrum-odw.de'
        message['To'] = requester
        smtp = smtplib.SMTP(SMTP_SERVER,port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        logging.debug(
            "Sending Mail with following tupel: %s" % (message))
        smtp.sendmail(message['From'], message['To'], message.as_string())
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error("The following error occured in send mail download: %s" % (err))
        return False
