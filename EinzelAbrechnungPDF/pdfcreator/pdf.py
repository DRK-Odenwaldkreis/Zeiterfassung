#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PDFOutput v 2.0

#Copyright Philipp Scior philipp.scior@drk-forum.de
#Adapted by Murat :-)

#contains all routines to print a nice pdf 

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

import sys
from fpdf import FPDF
import time
import os
import os.path
import datetime
sys.path.append("..")

from utils.pausen import calculate_net_shift_time
from utils.month import monthInt_to_string

FreeSans = './pdfcreator/FreeSans.ttf'
FreeSansBold = './pdfcreator/FreeSansBold.ttf'
Logo = '../utils/logo.png'
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
		# self.cell(40, 10, 'Impfzentrum Odenwaldkreis:', ln=0)
		self.image(Logo, x=7, y=10, w=100, h=24, type='PNG')
		self.cell(0, 10, datetime.date.today().strftime("%d.%m.%Y"), align='R', ln=1)
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, content, nachname, vorname, personalnummer, monat, year):
		self.content=content
		self.nachname=nachname
		self.vorname=vorname
		self.personalnummer=personalnummer
		self.date = datetime.date.today()
		self.year = year
		self.monat=monthInt_to_string(int(monat))
		self.totalSeconds = 0

	def generate(self):

		pdf=MyPDF()
		pdf.time = self.date
		# pdf.name=self.name
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.set_auto_page_break(True, 25)
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

		pdf.set_font('GNU', 'B', 14)

		pdf.cell(10, 10, '', ln=1)

		pdf.cell(20, 10, 'Arbeitszeitabrechnung', ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Mitarbeiter: {}'.format(self.nachname)+", "+self.vorname, ln=1)
		pdf.cell(20, 10, 'Personalnummer: {}'.format(self.personalnummer), ln=1)
		pdf.cell(20, 10, 'Arbeitszeitnachweis: {}'.format(self.monat)+", "+ self.year, ln=1)

		pdf.set_font('GNU', 'B' , 14)
		pdf.ln(10)
		pdf.cell(20, 10, 'Arbeitszeit:', 0, 1)

		pdf.cell(40, 10, 'Tag', 0, 0)
		pdf.cell(40, 10, 'Beginn', 0, 0)
		pdf.cell(40, 10, 'Ende', 0, 0)
		pdf.cell(40, 10, 'Art', 0, 0)
		pdf.cell(40, 10, 'Zeit', 0, 1)

		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)

		pdf.set_font('GNU', '', 14)


		for i in self.content:
			if pdf.y + 10 > pdf.page_break_trigger:
				pdf.set_font('GNU', 'B' , 14)
				pdf.cell(40, 10, 'Tag', 0, 0)
				pdf.cell(40, 10, 'Beginn', 0, 0)
				pdf.cell(40, 10, 'Ende', 0, 0)
				pdf.cell(40, 10, 'Art', 0, 0)
				pdf.cell(40, 10, 'Zeit', 0, 1)
				current_x =pdf.get_x()
				current_y =pdf.get_y()
				pdf.line(current_x, current_y, current_x+190, current_y)
				pdf.set_font('GNU', '', 14)
			self.begin = i[0].strftime("%H:%M")
			self.ende = i[1].strftime("%H:%M")
			self.netShiftTime, self.netShiftTimeHours, self.netShiftTimeMinutes = calculate_net_shift_time(i[0], i[1])
			self.totalSeconds = self.totalSeconds + int(self.netShiftTime.seconds)
			if self.netShiftTimeMinutes < 10:
				self.netShiftTimeMinutes = '0%s' % (self.netShiftTimeMinutes)
			pdf.cell(40, 10, i[0].strftime("%d.%m.%Y"),0,0)
			pdf.cell(40, 10, self.begin, 0, 0)
			pdf.cell(40, 10, self.ende, 0, 0)
			pdf.cell(40, 10, i[2], 0, 0)
			pdf.cell(40, 10, '%s:%s' %(self.netShiftTimeHours, self.netShiftTimeMinutes), 0, 1)
		self.totalHours, self.remainder = divmod(self.totalSeconds, 3600)
		self.totalMinutes, self.rest = divmod(self.remainder, 60)
		if self.totalMinutes < 10:
			self.totalMinutes = '0%s' % (self.totalMinutes)
		current_x =pdf.get_x()
		current_y =pdf.get_y()
		pdf.line(current_x, current_y, current_x+190, current_y)
		pdf.set_font('GNU', 'B' , 14)
		pdf.cell(135,20,'',0,0)
		pdf.cell(25,20,'Summe = ',0,0)
		pdf.cell(40, 20, '%s:%s' % (self.totalHours, self.totalMinutes), 0, 1)
		self.filename = "../../Reports/Einzelnachweis_" + self.monat + '_' + self.year + '_' + str(self.personalnummer) +"_" + self.nachname + "_" + self.vorname + ".pdf"
		pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
