#!/var/python

import os
import re
import sys
import time
import json
import client
from datetime import datetime

score = {}
with open('emo-list.txt','r') as source:
    score = { chr(int(c)):{ 'total':0, 'positive':0, 'negative':0 }
              for c in source.read().strip().split() }

labels = ('positive','negative')
stats = { 'total':0 }

options = [
    ('best','worst'),
    ('awesome','awful'),
    ('wonderful','terrible'),
    ('success','failure'),
    ('perfect','fault'),
    ('tesoro','basura'),
    ('люблю','ненавижу')]

insert = """
INSERT INTO emo_sent (code, span, <label>, total)
    VALUES('{}', '{}', {}, {})
    ON DUPLICATE KEY UPDATE
    <label> = <label> + VALUES(<label>),
    total = total + VALUES(total);
    """

update = """
UPDATE emo_sent a INNER JOIN (
    SELECT span, IF(negative > 0 AND positive > 0, positive/negative, 1) as ratio
    FROM emo_job_stats) as b USING(span)
SET a.sentiment = (a.positive - a.negative * b.ratio)/(a.positive + a.negative * b.ratio)
    WHERE a.span = '{}' AND a.total > 0;
    """

job_update = """
INSERT INTO emo_job_stats(span, <label>)
    VALUES('{}', {})
    ON DUPLICATE KEY UPDATE
    <label> = <label> + VALUES(<label>);
    """

def extract(label):
    def extract_set(data):
        try:
            obj = json.loads(data)
            if 'text' in obj and len(obj['text'].split()) < 10:
                #print(obj['text'])
                emo = { c:1 for c in obj['text'].lower() if c in score }
                for e in emo:
                    score[e]['total'] += 1
                    score[e][label] += 1
                stats['total'] += 1
        except:
            print('Error: {}'.format(sys.exc_info()))
    return extract_set


if  __name__ =='__main__':
    '''
    called by emo-job.sh:
    python emo-job.py <MINUTES RUN> <LABEL INDEX> <RANDOM OPTION INDEX>
    '''
    minutes = 5
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        minutes = int(sys.argv[1])

    label = 0
    if len(sys.argv) > 2 and int(sys.argv[2]) < len(labels):
        label = int(sys.argv[2])

    idx = 0
    if len(sys.argv) > 3 and int(sys.argv[3]) < len(options):
        idx = int(sys.argv[3])

    query = options[idx][label]
    label = labels[label]
    span = datetime.now().strftime('%Y-%m')

    twitter = client.TwitterClient()
    twitter.stream(query, broadcast = extract(label), timer = 60 * minutes)
    time.sleep(60 * minutes)
    with open('emo-job-update.sql','w') as output:
        for c,s in score.items():
            if s['total'] > 0:
                output.write(re.sub(r'\n\s+', ' ', re.sub('<label>', label,
                    insert.format(str(ord(c)), span, s[label], s['total']))))
        output.write(re.sub(r'\n\s+', ' ', update.format(span)))
        output.write(re.sub(r'\n\s+', ' ', re.sub('<label>', label,
                        job_update.format(span, stats['total']))))
