#!/bin/bash
echo "Begin sql dump"
mysqldump impfzentrum > /home/scior/impfzentrum.sql
echo "sql dump completed"