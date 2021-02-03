#!/bin/bash

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

echo "Starting check for new Dienstplaene with hysterese"
if [[ -n $(find /home/webservice/Planung/* -amin +239 -amin -299) ]]
then
echo "Result is true"
year=$(find /home/webservice/Planung/* -amin +239 -amin -299 | cut -d'/' -f5 | cut -d'_' -f2)
week=$(find /home/webservice/Planung/* -amin +239 -amin -299 | cut -d'/' -f5 | cut -d'_' -f4 | cut -d'.' -f1)
echo $year
echo $week
python3 ./job.py $week $year
else
echo "Result is false"
fi
echo "Checking done"