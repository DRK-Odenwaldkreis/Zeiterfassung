#!/usr/bin/python3
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
sys.path.append("..")

from utils.readconfig import read_config

FROM_EMAIL = read_config("Mail", "FROM_EMAIL")
TO_EMAIL = read_config("Mail", "TO_EMAIL")
SMTP_SERVER = read_config("Mail", "SMTP_SERVER")
SMTP_USERNAME = read_config("Mail", "SMTP_USERNAME")
SMTP_PASSWORD = read_config("Mail", "SMTP_PASSWORD")


def send_mail(day):
    try:
        message = MIMEMultipart()
        message.attach(MIMEText("Neuer Tagesreport wurde angelegt.",'plain'))
        message['Subject'] = "Neue Tagesreport für: %s" % (str(day))
        message['From'] = FROM_EMAIL
        message['To'] = str(TO_EMAIL)
        files = []
        files.append('../Reports/Tagesreport_%s.pdf' % (str(day)))
        for item in files:
            attachment = open(item, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= "+ item)
            message.attach(part)
        smtp = smtplib.SMTP(SMTP_SERVER)
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(message['From'], message['To'].split(",") , message.as_string())
        smtp.quit()
        return True
    except:
        print("Error in sendmail")
        return False