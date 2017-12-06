import os
import sys
import time
import json
import client


if  __name__ =='__main__':
    '''
    tweets with geo-data
    run: python stream-geo.py COUNT
    '''
    lim = False
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        lim = int(sys.argv[1])

    def extract(data):
        try:
            obj = json.loads(data)
            print('---------------------------------------------------')
            if obj['place'] is None: print('!!! NO PLACE DEFINED !!!')
            print(obj['place']['country_code'])
            print(obj['place']['full_name'])
            print(obj['place']['bounding_box'])
            print(obj['text'])
            print(obj['lang'])
        except:
            print('Error: {}'.format(sys.exc_info()))

    twitter = client.TwitterClient()
    twitter.stream('', geo = True, broadcast = extract, count = lim)
