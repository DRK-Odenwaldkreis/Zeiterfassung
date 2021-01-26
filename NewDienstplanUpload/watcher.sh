#!/bin/bash
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