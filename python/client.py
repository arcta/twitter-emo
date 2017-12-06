import os
import sys
from time import time
from tweepy import OAuthHandler, API, Stream, TweepError
from tweepy.streaming import StreamListener
from tweepy.parsers import JSONParser


class TwitterClient:
    def __init__(self):
        '''
        authenticate API
        '''
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
        except:
            print('Error: Authentication Failure')


    def sample(self, query, count = 10, geo = False):
        '''
        get sample data
        '''
        api = API(self.auth, parser = JSONParser())
        try:
            tweets = api.search(q = query, count = count)
            return tweets
        except TweepError as e:
            print('Error: {}'.format(e))
            return []


    class TweetListener(StreamListener):
        def __init__(self, broadcast, handle, count, timer):
            '''
            define broadcast and error-handle methods
            set count: how many tweets before disconnect
            set timer: seconds run before disconnect
            '''
            self.broadcast = broadcast
            self.handle = handle
            self.limit = count
            self.count = 0
            self.timer = time() + timer

        def on_data(self, data):
            self.broadcast(data)
            self.count += 1
            if self.limit and self.count > self.limit:
                return False  # disconnect: exceeded conf count
            if self.timer < time():
                return False  # disconnect: exceeded time limit
            return True

        def on_error(self, status):
            self.handle(status)
            if status == 420: # disconnect: exceeded API connection failure limit
                return False
            return True


    def stream(self,
               query, geo = False,
               broadcast = print, handle = print,
               count = False, timer = 60,
               async = True):
        '''
        stream tweets matching query with/or geo-filter
        '''
        if query == '': # get anything with geo
            geo = True
            keywords = []
        else:
            keywords = query.split(',')

        tweets = Stream(self.auth, self.TweetListener(broadcast, handle, count, timer))
        if geo:
            tweets.filter(track = keywords, locations = [-180,-90,180,90], async = async)
        else:
            tweets.filter(track = keywords, async = async)



if  __name__ =='__main__':
    print(TwitterClient())
