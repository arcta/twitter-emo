#!/bin/bash

########################################################################
# job calculating current and updating existing emoji sentiment score
# run: emo-job.sh <MINUTES RUN>
########################################################################
source ~/.local.cnf
cd ~/projects/twitter/python

if [ "$1" > 0 ]; then
    timer=$1
else
    timer=5
fi

((opt = (RANDOM % 10)))

mysql -u root -p$MYSQL_ROOT_PASS -B --disable-column-names -e \
"SELECT code FROM $DATABASE.emoji WHERE composite = 1" > emo-list.txt

echo "----- Positive index: $opt ----- Run: $timer minutes ------------"
python emo-job.py $timer 0 $opt
mysql -u root -p$MYSQL_ROOT_PASS $DATABASE < emo-job-update.sql

echo "----- Negative index: $opt ----- Run: $timer minutes ------------"
python emo-job.py $timer 1 $opt
mysql -u root -p$MYSQL_ROOT_PASS $DATABASE < emo-job-update.sql

mysql -u root -p$MYSQL_ROOT_PASS -B --disable-column-names -e "
SELECT a.chars, b.sentiment FROM emoji a JOIN emo_sent b USING(code)
WHERE b.span = DATE_FORMAT(CURDATE(), '%Y-%m') AND b.total > 0 ORDER BY b.sentiment
" > sentiment.txt
