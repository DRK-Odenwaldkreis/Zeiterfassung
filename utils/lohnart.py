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

import logging
import holidays
import datetime

logger = logging.getLogger('Leistungsart')
logger.debug('Logger for Leistungsartberechnung was initialised')
holidays = holidays.CountryHoliday('DE', prov='HE')

def get_lohnart(date, art):
    try:
        if art == "Krank":
            return 567
        elif art == "Urlaub":
            return 566
        elif art == "Rufbereitschaft":
            return 490
        elif art == "Normal":
            if date.weekday() < 6 and not date in holidays:
                return 490
            elif date.weekday() == 6 and not date in holidays:
                return 558
            elif date in holidays:
                return 556
            else:
                return 000
    except:
        return 000