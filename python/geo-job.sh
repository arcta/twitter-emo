#!/bin/bash

########################################################################
# job tracking daily emo geo counts by country
# run: geo-job.sh <MINUTES RUN>
########################################################################
source ~/.local.cnf
cd ~/projects/twitter/python

if [ "$1" > 0 ]; then
    timer=$1
else
    timer=3
fi

mysql -u root -p$MYSQL_ROOT_PASS -B --disable-column-names -e \
"SELECT code FROM $DATABASE.emoji WHERE composite = 1" > emo-list.txt

python geo-job.py $timer
mysql -u root -p$MYSQL_ROOT_PASS $DATABASE < geo-job-update.sql
