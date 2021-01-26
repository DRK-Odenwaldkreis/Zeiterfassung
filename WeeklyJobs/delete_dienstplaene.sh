#!/bin/bash
echo "Starting Cleanup of old Dienstplaene"
find /home/webservice/Dienstplaene/* -mtime +42 -exec rm {} \;
echo "Cleanup Done complete"