import sys
sys.path.append("..")
from database import Database
from pdfcreator.pdf import PDFgenerator
import datetime
import time
import locale

### TODO: 
# - Welches encoding genutzt wird muss in eine Config Datei
# - im pdfcreator: Wo die Schriftart liegt muss relativ angegeben werden

personalnummer = int(sys.argv[1])
monat= int(sys.argv[2])
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

daten = Database(0)

mitarbeiterZeiten = daten.monatsuebersicht_einzeln(personalnummer, monat)
nachname, vorname = daten.find_mitarbeiter(personalnummer)

input =[]
for i in mitarbeiterZeiten:
    anfang = datetime.datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S')
    ende = datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S')
    if int(i[4]) == 1:
        art="Arbeit"
    elif int(i[4]) == 2:
        art="Urlaub"
    else:
        art="Krank"
    # print((ende-anfang).seconds)
    t_raw_min = (ende-anfang).seconds/60
    if t_raw_min < 6*60:
        t=t_raw_min
    elif 6*60 <= t_raw_min < 9*60:
        t=t_raw_min-30
    else:
        t=t_raw_min-45

    input.append((anfang.date().strftime('%d.%m.%Y'), anfang.time().strftime('%H:%M'), ende.time().strftime('%H:%M'), t, art))


PDF = PDFgenerator(input, nachname, vorname, 6001, anfang.date().strftime('%B'), time.localtime())
PDF.generate()