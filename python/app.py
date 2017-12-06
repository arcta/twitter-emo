import os
import re
import sys
import time
import json
import nltk
import redis
import client
from textblob import TextBlob


if  __name__ =='__main__':
    '''
    QUERY: keyword1,keyword2,...
    run: python app.py QUERY GEO MINUTES
    '''
    pub = redis\
            .StrictRedis(password = os.environ['REDIS_PASS'],
                         host = os.environ['REDIS_HOST'],
                         port = os.environ['REDIS_PORT'],
                         db = 0)

    if os.path.isfile('/tmp/twitter.app'):
        pub.publish('twitter-app', 'active')

    else:
        query = ''
        if len(sys.argv) > 1:
            query = sys.argv[1]

        geo = False
        if len(sys.argv) > 2:
            geo = int(sys.argv[2]) > 0

        lim = 100
        if len(sys.argv) > 3 and int(sys.argv[3]) > 0:
            lim = max(100, min(int(sys.argv[3]), 1000))

        timer = 1
        if len(sys.argv) > 4 and int(sys.argv[4]) > 0:
            timer = max(1, min(int(sys.argv[4]), 10))

        emoji = {}
        with open('{}/twitter/python/sentiment.txt'.format(os.environ['PROJECTS_HOME']),'r') as source:
            for line in source.readlines():
                data = line.strip().split()
                emoji = { data[0]:float(data[1]) }
                print(data)

        stopwords = { word:1 for word in nltk.corpus.stopwords.words('english') }
        for lang in ['danish', 'dutch', 'finnish', 'french', 'german', 'hungarian', 'italian',
                     'norwegian', 'portuguese', 'russian', 'spanish', 'swedish', 'turkish']:
            for word in nltk.corpus.stopwords.words('spanish'): stopwords[word] = 1

        def extract(data):
            try:
                obj = json.loads(data)
                hashtags = ['#{}'.format(re.sub('\W+', '', term)) for term in obj['text'].split() if term[0] == '#']
                emo = [c for c in obj['text'] if str(ord(c)) in emoji]
                polarity = 0.
                words = re.sub('(@\S+)|(https?\://\S+)|([\W\d_]+)', ' ', obj['text'].lower()).split()
                words = [word for word in words if word not in stopwords]
                if obj['lang'] == 'en':
                    polarity = TextBlob(' '.join(words)).sentiment.polarity
                if len(emo) > 0:
                    score = [emoji[str(ord(c))] for c in emo]
                    if polarity != 0: score.append(polarity)
                    polarity = sum(score)/len(score)
                pub.publish('twitter-lang', obj['lang'])
                pub.publish('twitter-words', ','.join(words))
                pub.publish('twitter-emoji', ','.join(emoji))
                pub.publish('twitter-hashtags', ','.join(hashtags))
                pub.publish('twitter-sentiment', polarity)
                if 'place' in obj and obj['place'] is not None:
                    pub.publish('twitter-country', obj['place']['country_code'])
                    pub.publish('twitter-place', obj['place']['full_name'])
                    coords = obj['place']['bounding_box']['coordinates'][0]
                    w = coords[2][0] - coords[0][0]
                    h = coords[2][1] - coords[0][1]
                    pub.publish('twitter-box', '{:.4f},{:.4f},{:.4f},{:.4f},{:.3f}'\
                                .format(coords[0][0], coords[0][1], w, h, polarity))
                print(obj['text'])
            except:
                print('Error: {}'.format(sys.exc_info()))
                pass

        with open('/tmp/twitter.app','w') as output:
            output.write('RUNS: {}'.format(query))

        twitter = client.TwitterClient()
        twitter.stream(query, geo = geo, broadcast = extract, count = lim, timer = 10 * timer)
        time.sleep(10 * timer)
        os.remove('/tmp/twitter.app')
