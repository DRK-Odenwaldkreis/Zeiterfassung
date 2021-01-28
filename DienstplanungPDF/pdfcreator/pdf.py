#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PDFOutput v 2.0

#Copyright Philipp Scior philipp.scior@drk-forum.de
#Adapted by Murat :-)

#contains all routines to print a nice pdf 


import sys
from fpdf import FPDF
import time
import os
import os.path
import datetime
import logging
sys.path.append("..")

from utils.pausen import calculate_net_shift_time
from utils.day import dayInt_to_string



FreeSans = './pdfcreator/FreeSans.ttf'
FreeSansBold = './pdfcreator/FreeSansBold.ttf'
Logo = '../utils/genericLogo.png'

logger = logging.getLogger('Dienstplanung Report')

def get_week(y, w):
    first = next(
        (datetime.date(y, 1, 1) + datetime.timedelta(days=i)
         for i in range(367)
         if (datetime.date(y, 1, 1) + datetime.timedelta(days=i)).isocalendar()[1] == w))
    return [first + datetime.timedelta(days=i) for i in range(7)]

class MyPDF(FPDF):

    #it sucks that these members do not belong to specific object instances, but I can use __init__
    #since it overwrites the FPDF contructor and then shit does not work...
    # on the other hand this shouldnt be to bad for my case as the PDF generator only generates one
    # pdf at the time and time and name are set within the constructor for the PDF generator
	time='zeit'
	# name='name'


	def header(self):
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)
		self.image(Logo, x=7, y=10, w=100, h=24, type='PNG')
		self.cell(0, 10, 'Erzeugt am: %s'% datetime.date.today().strftime("%d.%m.%Y"), align='R', ln=1)
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, content, week, year):
		logger.debug('Starting the PDF Creation')
		self.content=content
		self.date = datetime.date.today()
		self.year = year
		logger.debug('Thats the year for planning: %s' %(self.year))
		self.week = week
		logger.debug('Thats the week for planning: %s' %(self.week))
		self.listOfDates = get_week(int(self.year), int(self.week))
		logger.debug('Thats the dates the planning is done for: %s'%(self.listOfDates))

	def write_lines(self, list):
		self.type = type
		self.list = list
		logger.debug('Writing the following pre-collected lines: %s' % (self.list))
		self.length = len(max(self.list, key=lambda coll: len(coll)))
		for line in range(0, self.length):
			if self.pdf.get_y() + 10 > self.pdf.page_break_trigger:
				logger.debug('Pagertrigger was achieved, creating new page.')
				self.new_page()
			else:
				for count, value in enumerate(self.list):
					if count == 0:
						logger.debug('Writing the frueh shift')
						try:
							self.pdf.cell(60, 10, value[line], ln=0)
						except:
							self.pdf.cell(60, 10, '', ln=0)
					elif count == 1:
						logger.debug('Writing the spaet shift')
						try:
							self.pdf.cell(60, 10, value[line], ln=0)
						except:
							self.pdf.cell(60, 10, '', ln=0)
					elif count == 2:
						logger.debug('Writing the variable shift')
						self.pdf.set_font('GNU', '', 10)
						try:
							self.pdf.cell(60, 10, value[line], ln=1)
						except:
							self.pdf.cell(60, 10, '', ln=1)
						finally:
							logger.debug('Resetting font size')
							self.pdf.set_font('GNU', '', 14)

	def new_page(self):
		self.pdf.add_font('GNU', '', FreeSans, uni=True)
		self.pdf.add_font('GNU', 'B', FreeSansBold, uni=True)
		self.pdf.set_font('GNU', 'B', 14)
		self.pdf.cell(20, 10, '', ln=1)
		self.pdf.cell(20, 10, '%s - %s' %
                    (dayInt_to_string(self.day.weekday()), self.day), ln=1)
		self.pdf.set_font('GNU', '', 14)
		self.pdf.cell(60, 10, 'Früh', ln=0)
		self.pdf.dashed_line(self.pdf.get_x()-5, self.pdf.get_y(),
                       self.pdf.get_x()-5, self.pdf.get_y()+210)
		self.pdf.cell(60, 10, 'Spät', ln=0)
		self.pdf.dashed_line(self.pdf.get_x()-5, self.pdf.get_y(),
                       self.pdf.get_x()-5, self.pdf.get_y()+210)
		self.pdf.cell(60, 10, 'Variabel', ln=1)
		self.pdf.line(self.pdf.get_x(), self.pdf.get_y(),
                    self.pdf.get_x()+180, self.pdf.get_y())
		self.pdf.cell(0, 1, '', ln=1)
		self.pdf.line(self.pdf.get_x(), self.pdf.get_y(),
                    self.pdf.get_x()+180, self.pdf.get_y())

	def create_day(self, day):
		self.day = day
		logger.debug('Starting the creation of the page for: %s' %(self.day))
		self.leftColumn = []
		self.centerColumn = []
		self.rightColumn = []
		self.new_page()
		for i in self.content:
			logger.debug('Found the following entry: %s' % (str(i)))
			self.currentVorname = i[0]
			self.currentNachname = i[1]
			self.shift = i[2]
			self.currentDate = i[3]
			if self.currentDate == self.day:
				self.pdf.set_font('GNU', '', 14)
				if self.shift == 1:
					self.leftColumn.append('%s, %s' % (self.currentNachname, self.currentVorname))
				elif self.shift == 2:
					self.centerColumn.append('%s, %s' % (self.currentNachname, self.currentVorname))
				elif self.shift == 3:
					self.rightColumn.append('%s, %s - (%s)' % (self.currentNachname, self.currentVorname, i[4]))
				else:
					logger.warning('The given shift does not exist')
			else:
				# No planning entry is included for that day
				pass
		logger.debug('Finished with the content of day: %s'%(self.day))
		self.list = [self.leftColumn, self.centerColumn, self.rightColumn]
		self.write_lines(self.list)


	def generate(self):

		self.pdf=MyPDF()
		self.pdf.time = self.date
		self.pdf.alias_nb_pages()
		self.pdf.add_page()
		self.pdf.set_auto_page_break(True, 25)
		for i in self.listOfDates:
			self.create_day(i)
			if i != self.listOfDates[-1]:
				self.pdf.add_page()
		self.filename = "../../Planung/Planung_" + self.year + '_' + self.week + ".pdf"
		self.pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
