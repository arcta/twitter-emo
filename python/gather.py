import os
import re
import sys
import time
import json
import client
from datetime import date


if  __name__ =='__main__':

    lang = 'en'
    if len(sys.argv) > 1:
        lang = sys.argv[1]

    lim = 1000000
    if len(sys.argv) > 2:
        lim = int(sys.argv[2])
    
    score = {}
    with open('emo-list.txt','r') as source:
        score = { chr(int(c)):{ 'total':0, 'positive':0, 'negative':0 }
                      for c in source.read().strip().split() }

    with open('data/{}/{}.csv'.format(lang, date.today().isoformat()), 'w') as output:
        output.write('text,emo\n')
            
        def extract(data):
            try:
                obj = json.loads(data)
                if obj['lang'] == lang:
                    words = re.sub("'", '', re.sub('(@\S+)|(https?\://\S+)|([\W\d_]+)', ' ',
                                                   obj['text'].lower())).split()
                    if len(words) > 0:
                        emo = { c:1 for c in obj['text'].lower() if c in score }
                        emo = list(emo.keys())
                        if len(emo) > 0:
                            output.write('{},{}\n'.format(' '.join(words), ' '.join(emo)))
            except:
                pass

        twitter = client.TwitterClient()
        twitter.stream('', geo = False, broadcast = extract, count = lim, timer = 60)
