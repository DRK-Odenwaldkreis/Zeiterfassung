#!/usr/bin/python3
# coding=utf-8

import logging

logger = logging.getLogger('Pausenberechnung')
logger.debug('Logger for pausen berechnung was initialised')

def calculate_net_shift_time(start,end):
    net = end - start
    return net
