#!/bin/bash

echo "Starting Report"
cd /home/webservice/Zeiterfassung/TagesReportPDF
python3 job.py
echo "Reporting complete"