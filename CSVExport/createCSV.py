import sys
import csv

from datetime import datetime


def create_CSV(content,date):
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
            writeEntry.writerow(["[VARTAB]",
                                 "INSERT",
                                 "800",
                                 "4",
                                 i[0],
                                 i[4],
                                 i[3],
                                 "1",
                                 "LA",
                                 "",
                                 "VD_ESTD",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "VD_DAT",
                                 "VD_ZDAT",
                                 "IMPVAR1",
                                 "VD_HER_DAT"
                                 ])
