#!/usr/bin/env python
# -*- coding: utf-8 -*-

#PDFOutput v 1.0

#Copyright Philipp Scior philipp.scior@drk-forum.de

#contains all routines to print 



from fpdf import FPDF
import time
import os
import os.path

FreeSans=os.path.join(os.getcwd(), '/Users/philippscior/Zeiterfassung/pdfcreator/FreeSans.ttf')   
FreeSansBold = os.path.join(os.getcwd(), '/Users/philippscior/Zeiterfassung/pdfcreator/FreeSansBold.ttf')

class MyPDF(FPDF):

    #it sucks that these members do not belong to specific object instances, but I can use __init__
    #since it overwrites the FPDF contructor and then shit does not work...
    # on the other hand this shouldnt be to bad for my case as the PDF generator only generates one
    # pdf at the time and time and name are set within the constructor for the PDF generator
	time='zeit'
	name='name'


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

	def __init__(self, content, name, monat, time):
		self.content=content
		self.name=name
		self.time=time
		self.monat=monat
		self.gesamt=0
		for i in self.content:
			self.gesamt += i[3]




	def generate(self):

		pdf=MyPDF()
		pdf.time=self.time
		pdf.name=self.name
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

		pdf.set_font('GNU', 'B', 14)

		pdf.cell(20, 10, 'Arbeitszeitabrechnung', ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Mitarbeiter: {}'.format(self.name), ln=1)
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
		pdf.cell(135,10,'',0,0)
		pdf.cell(25,10,'Summe = ',0,0)
		pdf.cell(40,10,'{},{} h'.format(int(self.gesamt/60),int((self.gesamt%60)/6*10)),0,1,)

		pdf.output(self.name+".pdf")

	# def orders(self, dest, order):
	# 	pdf=MyPDF()
	# 	pdf.time=self.time
	# 	pdf.name=self.name
	# 	pdf.alias_nb_pages()
	# 	for j in self.content:
	# 		if j[3]==1 and len(self.content)> 1:
	# 			pdf.add_page()
	# 			pdf.add_font('GNU', '', FreeSans, uni=True)
	# 			pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

	# 			pdf.set_font('GNU', '', 14)

	# 			header_name='Bereitstellungsraum '+self.name

	# 			pdf.cell(20, 10, 'von:', 0, 0)
	# 			pdf.cell(20, 10, header_name, ln=1)
	# 			pdf.cell(20, 10, 'an:', 0, 0)
	# 			pdf.cell(20, 10, j[0], ln=1)
	# 			pdf.cell(20, 10, 'Zeit:', 0, 0)
	# 			pdf.cell(20, 10, time.strftime("%d%H%M%b%Y", self.time)+'  |  '+time.strftime("%d %b %Y %H:%M", self.time), 0, 1)

	# 			pdf.set_font('GNU', 'B' , 14)
	# 			pdf.ln(10)
	# 			pdf.cell(20, 10, 'Auftrag / Marschbefehl:', 0, 1)
	# 			pdf.cell(20, 10, 'Ziel:', 0, 0)
	# 			pdf.set_font('GNU', '' , 14)
	# 			pdf.cell(20, 10, dest, ln=1)
	# 			pdf.set_font('GNU', 'B' , 14)
	# 			pdf.cell(20, 10, 'Beschreibung:', 0, 1)
	# 			pdf.set_font('GNU', '' , 14)
	# 			pdf.multi_cell(0, 10, order)

	# 			pdf.set_font('GNU', 'B' , 14)
	# 			pdf.cell(20, 10, 'Zu verlegende Einheiten:', 0, 1)
	# 			for i in self.content:
	# 				pdf.set_font('GNU', '', 10)     
	# 				pdf.cell(50, 10, i[0], 0, 0)
	# 				pdf.cell(40, 10, i[1], 0, 0)
	# 				pdf.cell(20, 10, i[2], 0, 0)
	# 				pdf.cell(50, 10, i[4], 0, 1)
	# 		else:
	# 			pass
	# 		pdf.add_page()
	# 		pdf.add_font('GNU', '', FreeSans, uni=True)
	# 		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

	# 		pdf.set_font('GNU', '', 14)

	# 		header_name='Bereitstellungsraum '+self.name

	# 		pdf.cell(20, 10, 'von:', 0, 0)
	# 		pdf.cell(20, 10, header_name, ln=1)
	# 		pdf.cell(20, 10, 'an:', 0, 0)
	# 		pdf.cell(20, 10, j[0], ln=1)
	# 		pdf.cell(20, 10, 'Zeit:', 0, 0)
	# 		pdf.cell(20, 10, time.strftime("%d%H%M%b%Y", self.time)+'  |  '+time.strftime("%d %b %Y %H:%M", self.time), 0, 1)

	# 		pdf.set_font('GNU', 'B' , 14)
	# 		pdf.ln(10)
	# 		pdf.cell(20, 10, 'Auftrag / Marschbefehl:', 0, 1)
	# 		pdf.cell(20, 10, 'Ziel:', 0, 0)
	# 		pdf.set_font('GNU', '' , 14)
	# 		pdf.cell(20, 10, dest, ln=1)
	# 		pdf.set_font('GNU', 'B' , 14)
	# 		pdf.cell(20, 10, 'Beschreibung:', 0, 1)
	# 		pdf.set_font('GNU', '' , 14)
	# 		pdf.multi_cell(0, 10, order)

	# 	string="{}".format(time.strftime("%d%H%M%b%Y", self.time))+"Auftrag"

	# 	if os.path.isfile(string+".pdf"):
	# 		string=string+"_{}s".format(time.strftime("%S", self.time))


	# 	pdf.output(string+".pdf")



            


	# def history(self):
	# 	pdf=MyLandscape()
	# 	print(FreeSans)
	# 	pdf.time=self.time
	# 	pdf.name=self.name
	# 	pdf.alias_nb_pages()
	# 	pdf.add_page(orientation='L')
	# 	#print(os.path.join(os.path.dirname(os.path.abspath(__file__)),'DejaVuSans.ttf'))
		
	# 	pdf.add_font('GNU', '', FreeSans, uni=True)
	# 	pdf.add_font('GNU', 'B', FreeSansBold, uni=True)
	# 	pdf.set_font('GNU', 'B' , 14)

	# 	pdf.cell(20, 10, 'Protokoll:', 0, 1)

	# 	pdf.cell(50, 10, 'Funkrufname', 0, 0)
	# 	pdf.cell(40, 10, 'Organisation', 0, 0)
	# 	pdf.cell(20, 10, 'Typ', 0, 0)
	# 	pdf.cell(30, 10, 'Ankunft', 0, 0)
	# 	pdf.cell(30, 10, 'Abfahrt', 0, 0)#
	# 	pdf.cell(30, 10, 'Ziel', 0, 0)
	# 	pdf.cell(35, 10, 'Besatzung', 0, 0)
	# 	pdf.cell(50, 10, 'Bemerkung', 0, 1)

	# 	current_x =pdf.get_x()
	# 	current_y =pdf.get_y()

	# 	pdf.line(current_x, current_y, current_x+275, current_y)

	# 	pdf.set_font('GNU', '', 14)

	# 	for i in self.content:
	# 		if pdf.y + 10 > pdf.page_break_trigger:
	# 			pdf.set_font('GNU', 'B' , 14)

	# 			pdf.cell(20, 10, 'Protokoll:', 0, 1)

	# 			pdf.cell(50, 10, 'Funkrufname', 0, 0)
	# 			pdf.cell(35, 10, 'Organisation', 0, 0)
	# 			pdf.cell(20, 10, 'Typ', 0, 0)
	# 			pdf.cell(30, 10, 'Ankunft', 0, 0)
	# 			pdf.cell(35, 10, 'Abfahrt', 0, 0)#
	# 			pdf.cell(30, 10, 'Ziel', 0, 0)
	# 			pdf.cell(35, 10, 'Besatzung', 0, 0)
	# 			pdf.cell(50, 10, 'Bemerkung', 0, 1)

	# 			current_x =pdf.get_x()
	# 			current_y =pdf.get_y()

	# 			pdf.line(current_x, current_y, current_x+275, current_y)

	# 			pdf.set_font('GNU', '', 14)
	# 		else:

	# 			pdf.set_font('GNU', '', 10)		
	# 			pdf.cell(50, 10, i[1], 0, 0)
	# 			pdf.cell(40, 10, i[2], 0, 0)
	# 			pdf.cell(20, 10, i[3], 0, 0)
	# 			pdf.cell(30, 10, i[8][:-10], 0, 0)
	# 			pdf.cell(30, 10, i[9][:-10], 0, 0)#
	# 			pdf.cell(30, 10, i[10], 0, 0)
	# 			pdf.cell(35, 10, '{}/{}/{}'.format(i[4],i[5],i[6]), 0, 0)
	# 			pdf.cell(50, 10, i[11], 0, 1)

	# 	pdf.output(self.name+"_protokoll.pdf")


aux=FPDF('P', 'mm', 'A4')

class MyLandscape(FPDF):
	time='zeit'
	name='name'
	

	def header(self):
		print(FreeSans)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('Arial', '', 11)
		self.cell(40, 10, 'Bereitstellungsraum:', ln=0)
		self.cell(10, 10, self.name, ln=0)
		self.cell(0,10, time.strftime("%d%H%M%b%Y", self.time), align='R', ln=1)
		self.ln(10)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)
		self.cell(40,10, 'generiert durch START:QR', ln=0)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')