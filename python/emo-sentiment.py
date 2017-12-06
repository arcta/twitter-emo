import os
import re
import sys
import time
import json
import client

from utils import score, labels, insert, update, extract


if  __name__ =='__main__':
    '''
    called by emo-sentiment.sh:
    emo-sentiment.py <LABEL> <KEYWORD> <MINUTES RUN>
    '''
    label = 'positive'
    if len(sys.argv) > 1 and sys.argv[1] in labels:
        label = sys.argv[1]

    query = 'best'
    if len(sys.argv) > 2:
        query = sys.argv[2]

    minutes = 5
    if len(sys.argv) > 3 and int(sys.argv[3]) > 0:
        minutes = int(sys.argv[3])

    span = datetime.now().strftime('%Y-%m')

    twitter = client.TwitterClient()
    twitter.stream(query, broadcast = extract(label), timer = 60 * minutes)
    time.sleep(60 * minutes)
    with open('emo-update.sql','w') as output:
        for c,s in score.items():
            if s['total'] > 0:
                output.write(re.sub(r'\n\s+', ' ', re.sub('<label>', label,
                    insert.format(str(ord(c)), span, s[label], s['total']))))
        output.write(re.sub(r'\n\s+', ' ', update.format(span)))
