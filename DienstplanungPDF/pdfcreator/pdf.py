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
sys.path.append("..")

from utils.pausen import calculate_net_shift_time
from utils.day import dayInt_to_string



FreeSans = './pdfcreator/FreeSans.ttf'
FreeSansBold = './pdfcreator/FreeSansBold.ttf'
Logo = '../utils/genericLogo.png'


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
		self.content=content
		self.date = datetime.date.today()
		self.year = year
		self.week = week
		self.listOfDates = get_week(int(self.year), int(self.week))
	
	def createDay(self, day):
		self.day = day
		self.pdf.add_font('GNU', '', FreeSans, uni=True)
		self.pdf.add_font('GNU', 'B', FreeSansBold, uni=True)
		self.pdf.set_font('GNU', 'B', 14)
		self.pdf.cell(20, 10, '', ln=1)
		self.pdf.cell(20, 10, '%s - %s' %
                    (dayInt_to_string(self.day.weekday()), self.day), ln=1)
		self.pdf.set_font('GNU', '', 14)
		self.current_x = self.pdf.get_x()
		self.current_y = self.pdf.get_y()
		self.pdf.line(self.current_x, self.current_y, self.current_x+60, self.current_y)
		for i in self.content:
			self.currentVorname = i[0]
			self.currentNachname = i[1]
			self.shift = i[2]
			self.currentDate = i[3]
			if self.currentDate == self.day:
				self.pdf.set_font('GNU', '', 14)
				self.pdf.cell(40, 10, '%s,%s'%(self.currentNachname,self.currentVorname), 0, 1)
			else:
				pass
				#print(False)
		self.pdf.add_page()


	def generate(self):

		self.pdf=MyPDF()
		self.pdf.time = self.date
		self.pdf.alias_nb_pages()
		self.pdf.add_page()
		self.pdf.set_auto_page_break(True, 25)
		for i in self.listOfDates:
			self.createDay(i)
		self.filename = "../../Planung/Planung_" + self.year + '_' + self.week + ".pdf"
		self.pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
