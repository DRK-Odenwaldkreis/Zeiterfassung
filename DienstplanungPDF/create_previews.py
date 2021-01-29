
import datetime
import os
import logging

logFile = '../../Logs/planning.log'
logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Dienstplanung Report')
logger.debug('Starting')


today = datetime.datetime.today()
for i in range(2,9):
    previewWeek = int((today + datetime.timedelta(days=i*7)).strftime("%V"))
    previewYear = int((today + datetime.timedelta(days=i*7)).strftime("%G"))
    logger.debug('Starting planning for KW: %s and Year: %s' % (previewWeek))
    os.system("python3 ./job.py %s %s"%(previewWeek,previewYear))
