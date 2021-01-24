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
from utils.month import monthInt_to_string

FreeSans = './pdfcreator/FreeSans.ttf'
FreeSansBold = './pdfcreator/FreeSansBold.ttf'
Logo = '../utils/genericLogo.png'
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

	def __init__(self, content, week, year):
		self.content=content
		self.date = datetime.date.today()
		self.year = year
		self.week = week

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

		pdf.cell(20, 10, 'Planung', ln=1)

		pdf.set_font('GNU', '', 14)


		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)

		pdf.set_font('GNU', '', 14)
		self.filename = "../../Planung/Planung_"  + self.year + '_' + self.week + ".pdf"
		pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
