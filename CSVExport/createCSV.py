import sys
import csv

from datetime import datetime
sys.path.append("..")
from utils.pausen import calculate_net_shift_time
from utils.lohnart import get_lohnart

netShiftTime=0
netShiftTimeHours=0
netShiftTimeMinutes=0

def create_CSV(content,month,year):
    with open('../Exports/export.csv', mode='w', newline='') as csvfile:
        writeEntry = csv.writer(csvfile, delimiter=';')
        writeEntry.writerow(["Satzart", 
                             "Funktion",
                             "MAN",
                             "AK",
                             "PNR",
                             "Name",
                             "Vorname",
                             "VERTNR",
                             "LA",
                             "VD_ETAGE",
                             "VD_ESTD",
                             "VD_EFAKT",
                             "VD_EBETRAG",
                             "KST",
                             "KOSTART",
                             "VD_KTR",
                             "VD_DAT",
                             "VD_ZDAT",
                             "VD_HER",
                             "VD_HER_DAT"
                             ])
        for i in content:
            netShiftTime, netShiftTimeHours, netShiftTimeMinutes = calculate_net_shift_time(i[1],i[2])
            lohnart = get_lohnart(i[1],i[5])
            writeEntry.writerow(["[VARTAB]",
                                 "INSERT",
                                 "800",
                                 "4",
                                 i[0],
                                 i[4],
                                 i[3],
                                 "1",
                                 lohnart,
                                 "",
                                 round(netShiftTime.seconds/3600, 2),
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 i[1].replace(day=1).strftime("%d/%m/%Y"),
                                 i[1].replace(day=1).replace(month=int(month)+1).strftime("%d/%m/%Y"),
                                 "IMPVAR1",
                                 i[1].replace(day=1).strftime("%d/%m/%Y")
                                 ])
