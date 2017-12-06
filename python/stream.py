import os
import sys
import client


if  __name__ =='__main__':
    '''
    QUERY: keyword1,keyword2,...
    run: python stream.py QUERY GEO
    '''
    query = ''
    if len(sys.argv) > 1:
        query = sys.argv[1]

    geo = False
    if len(sys.argv) > 2:
        geo = True

    twitter = client.TwitterClient()
    twitter.stream(query, geo = geo)
