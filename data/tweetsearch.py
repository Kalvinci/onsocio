#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv



#Twitter API credentials
consumer_key = "QJMv5JMtygcJP1b4mdiO0j7G6"
consumer_secret = "j2Kb1UXIiidhURgw3aTfcLyFWCIBQJrAd8XUEDDBn6Nw4vgqEB"
access_key = "2780669995-2utlBroP7o04duf0oR9C3MdbU28VzEWVtrS0Usc"
access_secret = "PAsP6iTlvul4EdBw8qKKeqE6OB0OP84BDRmp74HhqiMkS"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
query = 'isis politics'
max_tweets = 3000
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        print(e)
        break

outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),tweet.retweet_count,tweet.favorite_count] for tweet in searched_tweets]
with open('political_tweets.csv', 'a') as f:
        writer = csv.writer(f)
        #writer.writerow(["id","created_at","text","retweet_count","favorite_count"])
        writer.writerows(outtweets)

print('done')