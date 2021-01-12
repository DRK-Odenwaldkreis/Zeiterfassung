#!/usr/bin/python3
# coding=utf-8
import os
import sys
import configparser

def read_config(section,variable):
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config.get(section,variable)
