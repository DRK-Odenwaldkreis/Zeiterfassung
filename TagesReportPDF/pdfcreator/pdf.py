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
LogoImpfen = '../utils/logo_impfen.png'
LogoTesten = '../utils/logo_testen.png'

FreeSans = '../utils/Schriftart/FreeSans.ttf'
FreeSansBold = '../utils/Schriftart/FreeSansBold.ttf'
	


class PDFgenerator(FPDF):

	def start(self, content, date, abrechnungskreis):
		self.content=content
		self.date=date
		if abrechnungskreis == '5':
			self.abrechnungskreis = 'Testzentrum'
		elif abrechnungskreis == '4':
			self.abrechnungskreis = 'Impfzentrum'
		else:
			self.abrechnungskreis = 'Test- und Impfzentrum'
		self.totalSeconds=0
	
	def header(self):
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)
		if self.abrechnungskreis == "Impfzentrum":
			self.cell(40, 10, 'Impfzentrum Odenwaldkreis:', ln=1)
			self.image(LogoImpfen, x=7, y=10, w=100, h=24, type='PNG')
		elif self.abrechnungskreis == "Testzentrum":
			self.cell(40, 10, 'Testzentrum Odenwaldkreis:', ln=1)
			self.image(LogoTesten, x=7, y=10, w=100, h=24, type='PNG')
		else :
			self.cell(40, 10, 'Test- und Impfzentrum Odenwaldkreis:', ln=1)
			self.image(LogoImpfen, x=7, y=10, w=100, h=24, type='PNG')
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


	def generate(self):

		#self.time=self.date
		# self.name=self.name
		self.alias_nb_pages()
		self.add_page()
		self.set_auto_page_break(True, 25)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.add_font('GNU', 'B', FreeSansBold, uni=True)
		
		self.set_font('GNU', 'B', 14)
		self.cell(20, 10, 'Tagesprotokoll für das %s am %s' % (self.abrechnungskreis,self.date), ln=1)

		self.set_font('GNU', '', 14)

		self.cell(20, 10, 'Erstellt: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d um %H:%M:%S"), ln=1))
		self.set_text_color(255,0,0)
		self.cell(0,10, 'Rote Einträge prüfen', align='R', ln=1)
		self.set_text_color(0,0,0)
		self.set_font('GNU', 'B' , 20)
		self.ln(15)
		self.cell(20, 10, 'Dienste:', 0, 1)
		self.set_font('GNU', 'B', 14)
		self.cell(35, 10, 'Personal-Nr.', 0, 0)
		self.cell(35, 10, 'Nachname', 0, 0)
		self.cell(35, 10, 'Beginn', 0, 0)
		self.cell(35, 10, 'Ende', 0, 0)
		self.cell(35, 10, 'Art', 0, 0)
		self.cell(35, 10, 'Zeit', 0, 1)


		current_x =self.get_x()
		current_y =self.get_y()

		self.line(current_x, current_y, current_x+190, current_y)

		self.set_font('GNU', '', 14)
		

		for i in self.content:
			if self.y + 10 > self.page_break_trigger:
				self.set_font('GNU', 'B', 14)
				self.ln(10)
				self.cell(35, 10, 'Personal-Nr.', 0, 0)
				self.cell(35, 10, 'Nachname', 0, 0)
				self.cell(35, 10, 'Beginn', 0, 0)
				self.cell(35, 10, 'Ende', 0, 0)
				self.cell(35, 10, 'Art', 0, 0)
				self.cell(35, 10, 'Zeit', 0, 1)
				current_x =self.get_x()
				current_y =self.get_y()
				self.line(current_x, current_y, current_x+190, current_y)
				self.set_font('GNU', '', 14)
			if i[6] == 1:
				self.set_text_color(255,0,0)
			else:
				self.set_text_color(0, 0, 0)
			self.begin = i[1].strftime("%H:%M")
			self.ende = i[2].strftime("%H:%M")
			self.netShiftTime, self.netShiftTimeHours, self.netShiftTimeMinutes, self.breakTime = calculate_net_shift_time(
				i[1], i[2])
			self.totalSeconds = self.totalSeconds + int(self.netShiftTime.seconds)
			if self.netShiftTimeMinutes < 10:
				self.netShiftTimeMinutes = '0%s' % (self.netShiftTimeMinutes)
			self.cell(35, 10, str(i[0]), 0, 0)
			#self.cell(40, 10, str(i[3]), 0, 0)
			self.cell(35, 10, str(i[4][:15]), 0, 0)
			self.cell(35, 10, self.begin, 0, 0)
			self.cell(35, 10, self.ende, 0, 0)
			self.cell(35, 10, str(i[5]), 0, 0)
			self.cell(35,10,'%s:%s' % (self.netShiftTimeHours,self.netShiftTimeMinutes),0,1)
			self.set_text_color(0, 0, 0)
		self.totalHours, self.remainder = divmod(self.totalSeconds, 3600)
		self.totalMinutes, self.rest = divmod(self.remainder, 60)
		if self.totalMinutes < 10:
			self.totalMinutes = '0%s' % (self.totalMinutes)
		current_x =self.get_x()
		current_y =self.get_y()
		self.line(current_x, current_y, current_x+190, current_y)
		self.set_font('GNU', 'B' , 14)
		self.cell(135,20,'',0,0)
		self.cell(40,20,'Gesamtsumme',0,0)
		self.cell(40, 20, '%s:%s' % (self.totalHours, self.totalMinutes), 0, 1)
		self.filename = "../../Reports/Tagesreport_" + self.abrechnungskreis + "_" + str(self.date) + ".pdf"
		self.output(self.filename)
		return self.filename.replace('../../Reports/','')

aux=FPDF('P', 'mm', 'A4')
