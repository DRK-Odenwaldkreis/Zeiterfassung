from dummy_database.database import Database
from pdfcreator.pdf import PDFgenerator
import datetime
import time
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

Daten = Database(0)

bayram = Daten.monatsuebersicht_einzeln(6001,1)
print(bayram)
input =[]
for i in bayram:
    anfang = datetime.datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S')
    ende = datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S')
    if int(i[4]) == 1:
        art="normal"
    elif int(i[4]) == 2:
        art="Urlaub"
    else:
        art="krank"
    # print((ende-anfang).seconds)

    input.append((anfang.date().strftime('%d.%m.%Y'), anfang.time().strftime('%H:%M'), ende.time().strftime('%H:%M'), (ende-anfang).seconds/60, art))
print(input)

PDF = PDFgenerator(input, "Bayram, Murat", anfang.date().strftime('%B'), time.localtime())
PDF.generate()