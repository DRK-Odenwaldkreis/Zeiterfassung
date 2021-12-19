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

from os import path
import logging
import sys
sys.path.append("..")
from utils.database import Database

logFile = '../../Logs/rotationJob.log'
logging.basicConfig(filename=logFile, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Nightly Auto Clean')
logger.debug('Starting')

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Update Dienste SET Dienstende = current_timestamp(), AutoClosed = '1' WHERE Dienstende is NULL"
        logger.debug('Closing shift, using the following query: %s' % (sql))
        DatabaseConnect.update(sql)
        logger.debug('Done')
    except Exception as e:
        logging.error("Error")
    finally:
        DatabaseConnect.close_connection()
