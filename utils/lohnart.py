#!/usr/bin/python3
# coding=utf-8

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