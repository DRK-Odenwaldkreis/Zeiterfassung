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
