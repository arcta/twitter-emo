import os
import sys
import redis
import client


if  __name__ =='__main__':
    '''
    QUERY: keyword1,keyword2,...
    run: python stream-redis.py QUERY GEO LIM
    '''
    pub = redis\
        .StrictRedis(password = os.environ['REDIS_PASS'],
                     host = os.environ['REDIS_HOST'],
                     port = os.environ['REDIS_PORT'],
                     db = 0)
    query = ''
    if len(sys.argv) > 1:
        query = sys.argv[1]

    geo = False
    if len(sys.argv) > 2:
        geo = True

    lim = False
    if len(sys.argv) > 3 and int(sys.argv[3]) > 0:
        lim = int(sys.argv[3])

    twitter = client.TwitterClient()
    twitter.stream(query,
                   geo = geo,
                   broadcast = lambda data: pub.publish('twitter', data),
                   count = lim)
