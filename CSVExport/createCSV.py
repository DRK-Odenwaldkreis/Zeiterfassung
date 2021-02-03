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
import csv

from datetime import datetime
sys.path.append("..")
from utils.pausen import calculate_net_shift_time
from utils.lohnart import get_lohnart

netShiftTime=0
netShiftTimeHours=0
netShiftTimeMinutes=0

def create_CSV(content, month, year):
    filename = "../../Reports/export.csv"
    with open(filename, mode='w', newline='') as csvfile:
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
    return filename
