#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PDFOutput v 1.0

#Copyright Philipp Scior philipp.scior@drk-forum.de
#Adapted by Murat :-)

#contains all routines to print a nice pdf 



from fpdf import FPDF
import time
import os
import os.path
import datetime

FreeSans='./pdfcreator/FreeSans.ttf'
FreeSansBold = './pdfcreator/FreeSansBold.ttf'

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
		self.cell(40, 10, 'Impfzentrum Odenwaldkreis:', ln=0)
		#self.cell(0,10, time.strftime("%d.%m.%Y", self.time), align='R', ln=1)
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, content):
		self.content=content
		self.date=datetime.date.today()


	def generate(self):

		pdf=MyPDF()
		pdf.time=self.date
		# pdf.name=self.name
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)
		
		pdf.set_font('GNU', 'B', 14)
		pdf.cell(20, 10, 'Tagesprotokoll für den %s' % (self.date), ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Erstellt: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d um %H:%M:%S"), ln=1))

		pdf.set_font('GNU', 'B' , 20)
		pdf.ln(15)
		pdf.cell(20, 10, 'Dienste:', 0, 1)
		pdf.set_font('GNU', 'B', 14)
		pdf.cell(40, 10, 'Personal-Nr.', 0, 0)
		pdf.cell(40, 10, 'Nachname', 0, 0)
		pdf.cell(40, 10, 'Begin', 0, 0)
		pdf.cell(40, 10, 'Ende', 0, 0)
		pdf.cell(40, 10, 'Art', 0 ,0)


		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)

		pdf.set_font('GNU', '', 14)
		

		for i in self.content:
			if pdf.y + 10 > pdf.page_break_trigger:
				pdf.set_font('GNU', 'B' , 14)

				pdf.cell(40, 10, 'Personal-Nr.', 0, 0)
				pdf.cell(40, 10, 'Nachname', 0, 0)
				pdf.cell(40, 10, 'Begin', 0, 0)
				pdf.cell(40, 10, 'Ende', 0, 0)
				pdf.cell(40, 10, 'Art', 0 ,0)

				current_x =pdf.get_x()
				current_y =pdf.get_y()

				pdf.line(current_x, current_y, current_x+190, current_y)

				pdf.set_font('GNU', '', 14)
			else:
				if i[6] == 0:
					pdf.set_text_color(0, 0, 0)
				else:
					pdf.set_text_color(255,0,0)
				begin = str(i[1].time())
				ende = str(i[2].time())		
				pdf.cell(40, 10, str(i[0]), 0, 0)
				#pdf.cell(40, 10, str(i[3]), 0, 0)
				pdf.cell(40, 10, str(i[4]), 0, 0)
				pdf.cell(40, 10, begin, 0, 0)
				pdf.cell(40, 10, ende, 0, 0)
				pdf.cell(40, 10, str(i[5]), 0, 0)
				pdf.cell(40, 10, '{},{} h'.format(len(str(i[1]))/60,len(str(i[1]))%60/6*10), 0, 1)
				pdf.set_text_color(0, 0, 0)
		
		current_x =pdf.get_x()
		current_y =pdf.get_y()
		pdf.line(current_x, current_y, current_x+190, current_y)
		pdf.set_font('GNU', 'B' , 14)
		pdf.cell(135,20,'',0,0)
		#pdf.cell(40,20,'{},{} h'.format(int(self.gesamt/60),int((self.gesamt%60)/6*10)),0,1,)

		pdf.output("Tagesreport_" + str(self.date) + ".pdf")

aux=FPDF('P', 'mm', 'A4')
