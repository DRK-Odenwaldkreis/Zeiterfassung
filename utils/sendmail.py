#!/usr/bin/python3
# coding=utf-8

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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
import sys
import os
sys.path.append("..")

from utils.readconfig import read_config

logger = logging.getLogger('Send Mail')
logger.debug('Starting')

FROM_EMAIL = read_config("Mail", "FROM_EMAIL")
TO_EMAIL = read_config("Mail", "TO_EMAIL")
SMTP_SERVER = read_config("Mail", "SMTP_SERVER")
SMTP_USERNAME = read_config("Mail", "SMTP_USERNAME")
SMTP_PASSWORD = read_config("Mail", "SMTP_PASSWORD")


def send_mail_report(filename, day):
    try:
        logging.debug("Receviced the following filename %s to be sent." % (filename))
        message = MIMEMultipart()
        with open('../utils/MailLayout/NewReport.html', encoding='utf-8') as f:
            fileContent = f.read()
        messageContent = fileContent.replace('[[DAY]]', str(day))
        message.attach(MIMEText(messageContent, 'html'))
        recipients = ['testzentrum@drk-odenwaldkreis.de']
        message['Subject'] = "Neue Tagesreport für: %s" % (str(day))
        message['From'] = 'info@testzentrum-odenwald.de'
        message['reply-to'] = 'testzentrum@drk-odenwaldkreis.de'
        message['Cc'] = 'info@testzentrum-odenwald.de'
        message['To'] = ", ".join(recipients)
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
        smtp.send_message(message)
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
        with open('../utils/MailLayout/Reminder.html', encoding='utf-8') as f:
            fileContent = f.read()
        messageContent = fileContent.replace('[[KW]]',str(week)).replace('[[YEAR]]',str(year))
        message.attach(MIMEText(messageContent, 'html'))
        message['Subject'] = "Erinnerung für Planung KW %s in %s" % (str(week), str(year))
        message['From'] = 'planung@testzentrum-odenwald.de'
        message['reply-to']= 'testzentrum@drk-odenwaldkreis.de'
        message['Bcc'] = ", ".join(listRecipients)
        message['Cc'] = 'info@testzentrum-odenwald.de'
        smtp = smtplib.SMTP(SMTP_SERVER, port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)
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
        with open('../utils/MailLayout/NewDienstplan.html', encoding='utf-8') as f:
            fileContent = f.read()
        messageContent = fileContent.replace('[[KW]]',str(week)).replace('[[YEAR]]',str(year))
        message.attach(MIMEText(messageContent, 'html'))
        message['Subject'] = "Neue Planung für KW %s in %s" % (
            str(week), str(year))
        message['From'] = 'dienstplan@testzentrum-odenwald.de'
        message['Bcc'] = ", ".join(listRecipients)
        message['Cc'] = 'info@testzentrum-odenwald.de'
        message['reply-to']= 'testzentrum@drk-odenwaldkreis.de'
        smtp = smtplib.SMTP(SMTP_SERVER, port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)
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
        url = 'https://dienst.testzentrum-odw.de/download.php?file=' + str(filename)
        logging.debug("The created url is %s" % (url))
        with open('../utils/MailLayout/NewDownload.html', encoding='utf-8') as f:
            fileContent = f.read()
        messageContent = fileContent.replace('[[LINK]]', str(url))
        message.attach(MIMEText(messageContent, 'html'))        
        message['Subject'] = "Einzelnachweise sind zum Download verfügbar"
        message['From'] = 'info@testzentrum-odenwald.de'
        message['To'] = requester
        message['Cc'] = 'info@testzentrum-odenwald.de'
        smtp = smtplib.SMTP(SMTP_SERVER,port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        logging.debug(
            "Sending Mail with following tupel: %s" % (message))
        smtp.send_message(message)
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error("The following error occured in send mail download: %s" % (err))
        return False


def send_mail_csvexport_download(filename, requester):
    try:
        logging.debug("Receviced the following filename %s to be sent to %s" % (
            filename, requester))
        message = MIMEMultipart()
        url = 'https://dienst.testzentrum-odw.de/download.php?file=' + str(filename)
        logging.debug("The created url is %s" % (url))
        with open('../utils/MailLayout/NewExport.html', encoding='utf-8') as f:
            fileContent = f.read()
        messageContent = fileContent.replace('[[LINK]]', str(url))
        message.attach(MIMEText(messageContent, 'html'))
        message['Subject'] = "CSV Export ist zum Download verfügbar"
        message['From'] = 'info@testzentrum-odenwald.de'
        message['To'] = requester
        message['Cc'] = 'info@testzentrum-odenwald.de'
        smtp = smtplib.SMTP(SMTP_SERVER, port=587)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        logging.debug(
            "Sending Mail with following tupel: %s" % (message))
        smtp.send_message(message)
        logging.debug("Mail was send")
        smtp.quit()
        return True
    except Exception as err:
        logging.error(
            "The following error occured in send mail download: %s" % (err))
        return False
