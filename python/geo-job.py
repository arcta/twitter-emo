#!/var/python

import os
import re
import sys
import time
import json
import client
from datetime import datetime, timedelta


res = { 'count':{}, 'emo':[] }
score = {}
with open('emo-list.txt','r') as source:
    score = { chr(int(c)):{ 'total':0, 'positive':0, 'negative':0 }
              for c in source.read().strip().split() }

insert = """
INSERT INTO emo_stats (code, country_code, span, total)
    VALUES('{}', '{}', '{}', 1)
    ON DUPLICATE KEY UPDATE
    total = total + VALUES(total);
    """

update = """
INSERT INTO geo_sent(country_code, span, sentiment)
    SELECT d.country_code, d.span, SUM(d.rate * d.sentiment) as sentiment
    FROM (
        SELECT a.code, a.country_code, a.span,
               a.total/b.total as rate, b.total as support, c.sentiment
        FROM (SELECT code, country_code, span, SUM(total) as total
              FROM emo_stats
              WHERE span = CURDATE()
              GROUP BY code, country_code, span) as a
        INNER JOIN (SELECT country_code, SUM(total) as total
              FROM emo_stats
              GROUP BY country_code) as b
        USING(country_code)
        INNER JOIN (SELECT code, sentiment
              FROM emo_sent
              WHERE span = '{}' AND total > 10) as c
        USING(code)
        HAVING support > 10
    ) as d
    GROUP BY d.country_code, d.span
ON DUPLICATE KEY UPDATE sentiment = VALUES(sentiment);
    """

job_update = """
INSERT INTO geo_job_stats(country_code, span, total)
    VALUES('{}', '{}', {})
    ON DUPLICATE KEY UPDATE
    total = total + VALUES(total);
    """


def extract(data):
    try:
        obj = json.loads(data)
        if 'text' in obj and len(obj['text'].split()) < 10:
            c = '??'
            if 'place' in obj and 'country_code' in obj['place']:
                c = obj['place'].get('country_code', '??')

            #print(c, obj['text'])
            emo = { c:1 for c in obj['text'].lower() if c in score }
            for e in emo:
                res['emo'].append((e, c))

            res['count'][c] = res['count'].get(c, 0)
            res['count'][c] += 1
    except:
        print('Error: {}'.format(sys.exc_info()))


if  __name__ =='__main__':
    '''
    called by geo-job.sh:
    python geo-job.py <MINUTES RUN>
    '''
    minutes = 5
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        minutes = int(sys.argv[1])

    date = datetime.now().strftime('%Y-%m-%d')
    span = datetime.now().strftime('%Y-%m')
    if int(datetime.now().strftime('%d')) < 10:
        span = (datetime.now() - timedelta(days = 30)).strftime('%Y-%m')
    
    twitter = client.TwitterClient()
    twitter.stream('', geo = True, broadcast = extract, timer = 60 * minutes)
    time.sleep(60 * minutes)
    with open('geo-job-update.sql','w') as output:
        for e in res['emo']:
            output.write(re.sub(r'\n\s+', ' ',
                insert.format(str(ord(e[0])), e[1], date)))
        output.write(re.sub(r'\n\s+', ' ', update.format(span)))
        for c in res['count']:
            output.write(re.sub(r'\n\s+', ' ', job_update.format(c, date, res['count'][c])))
