#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PDFOutput v 1.0

#Copyright Philipp Scior philipp.scior@drk-forum.de

#contains all routines to print a nice pdf 



from fpdf import FPDF
import time
import os
import os.path

FreeSans=os.path.join(os.getcwd(), '/Users/philippscior/Zeiterfassung/EinzelAbrechnungPDF/pdfcreator/FreeSans.ttf')   
FreeSansBold = os.path.join(os.getcwd(), '/Users/philippscior/Zeiterfassung/EinzelAbrechnungPDF/pdfcreator/FreeSansBold.ttf')

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
		self.cell(0,10, time.strftime("%d.%m.%Y", self.time), align='R', ln=1)
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, content, nachname, vorname, personalnummer, monat, time):
		self.content=content
		self.nachname=nachname
		self.vorname=vorname
		self.personalnummer=personalnummer
		self.time=time
		self.monat=monat
		self.gesamt=0
		for i in self.content:
			self.gesamt += i[3]




	def generate(self):

		pdf=MyPDF()
		pdf.time=self.time
		# pdf.name=self.name
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.set_auto_page_break(True, 25)
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

		pdf.set_font('GNU', 'B', 14)

		pdf.cell(20, 10, 'Arbeitszeitabrechnung', ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Mitarbeiter: {}'.format(self.nachname)+", "+self.vorname, ln=1)
		pdf.cell(20, 10, 'Personalnummer: {}'.format(self.personalnummer), ln=1)
		pdf.cell(20, 10, 'Abrechnungszeitraum: {}'.format(self.monat), ln=1)

		pdf.set_font('GNU', 'B' , 14)
		pdf.ln(10)
		pdf.cell(20, 10, 'Arbeitszeit:', 0, 1)

		pdf.cell(40, 10, 'Tag', 0, 0)
		pdf.cell(40, 10, 'Begin', 0, 0)
		pdf.cell(40, 10, 'Ende', 0, 0)
		pdf.cell(40, 10, 'Art', 0 ,0)
		pdf.cell(40, 10, 'Zeit', 0, 1)

		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)

		pdf.set_font('GNU', '', 14)


		for i in self.content:
			if pdf.y + 10 > pdf.page_break_trigger:
				pdf.set_font('GNU', 'B' , 14)

				pdf.cell(40, 10, 'Tag', 0, 0)
				pdf.cell(40, 10, 'Begin', 0, 0)
				pdf.cell(40, 10, 'Ende', 0, 0)
				pdf.cell(40, 10, 'Art', 0 ,0)
				pdf.cell(40, 10, 'Zeit', 0, 1)

				current_x =pdf.get_x()
				current_y =pdf.get_y()

				pdf.line(current_x, current_y, current_x+190, current_y)

				pdf.set_font('GNU', '', 14)
			else:		
				pdf.cell(40, 10, i[0], 0, 0)
				pdf.cell(40, 10, i[1], 0, 0)
				pdf.cell(40, 10, i[2], 0, 0)
				pdf.cell(40, 10, i[4], 0, 0)
				pdf.cell(40, 10, '{},{} h'.format(int(i[3]/60),int((i[3]%60)/6*10)), 0, 1)
		
		current_x =pdf.get_x()
		current_y =pdf.get_y()
		pdf.line(current_x, current_y, current_x+190, current_y)
		pdf.set_font('GNU', 'B' , 14)
		pdf.cell(135,20,'',0,0)
		pdf.cell(25,20,'Summe = ',0,0)
		pdf.cell(40,20,'{},{} h'.format(int(self.gesamt/60),int((self.gesamt%60)/6*10)),0,1,)

		pdf.output(self.nachname+"_"+self.vorname+".pdf")

aux=FPDF('P', 'mm', 'A4')