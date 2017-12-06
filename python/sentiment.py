import os
import re
import sys
import time
import json
import client


labels = ('positive','negative')

options = [
    ('best','worst'),
    ('awesome','awful'),
    ('success','failure'),
    ('tesoro','basura'),
    ('люблю','ненавижу'),
    ('wonderful','terrible')]

insert = """
INSERT INTO emoji (code, <label>, total)
    VALUES('{}', {}, {})
    ON DUPLICATE KEY UPDATE
    <label> = <label> + VALUES(<label>),
    total = total + VALUES(total);
    """

update = """
UPDATE emoji
    SET sentiment = (positive - negative)/total
    WHERE total > 0;
    """

def extract(label):
    def extract_set(data):
        try:
            obj = json.loads(data)
            if 'text' in obj and len(obj['text'].split()) < 10:
                #print(obj['text'])
                emo = { c:1 for c in obj['text'].lower() if c in score }
                for c in emo:
                    score[c]['total'] += 1
                    score[c][label] += 1
        except:
            print('Error: {}'.format(sys.exc_info()))
    return extract_set


if  __name__ =='__main__':

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

    score = {}
    with open('codes.txt','r') as source:
        score = { chr(int(c)):{ 'total':0, label:0 }
                 for c in source.read().strip().split() }

    twitter = client.TwitterClient()
    twitter.stream(query, broadcast = extract(label), timer = 60 * minutes)
    time.sleep(60 * minutes)
    with open('update-emoji-score.sql','w') as output:
        for c,s in score.items():
            if s['total'] > 0:
                output.write(re.sub(r'\n\s+', ' ', re.sub('<label>', label,
                    insert.format(str(ord(c)), s[label], s['total']))))
        output.write(re.sub(r'\n\s+', ' ', update))
