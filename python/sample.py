import os
import sys
import client


if __name__ == "__main__":
    '''
    run: python sample.py QUERY COUNT GEO
    '''
    query = 'machine learning,AI'
    if len(sys.argv) > 1:
        query = sys.argv[1]

    count = 10
    if len(sys.argv) > 2:
        count = int(sys.argv[2])

    geo = False
    if len(sys.argv) > 3:
        geo = True

    twitter = client.TwitterClient()
    tweets = twitter.sample(query, count = count, geo = geo)
    print(tweets)
