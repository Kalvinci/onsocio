#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import internetChecker as check
import pickle
import classify as cla

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method



    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    if len(alltweets)!=0:
        oldest = alltweets[-1].id - 1
        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            if(len(alltweets)>=1000):
                break
            print("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print("...%s tweets downloaded so far" % (len(alltweets)))
            outtweets = [tweet.full_text for tweet in alltweets]
            file = open('App_Data/%s_tweets.pickle' % screen_name, 'wb')
            pickle.dump(outtweets, file)
            file.close()
    else:
        outtweets= [tweet.full_text for tweet in alltweets]
        file = open('App_Data/%s_tweets.pickle' % screen_name, 'wb')
        pickle.dump(outtweets,file)
        file.close()
    # transform the tweepy tweets into a 2D array that will populate the csv
    ''' outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.retweet_count, tweet.favorite_count]
                 for tweet in alltweets]

    # write the csv
    with open('App_Data/%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "retweet_count", "favorite_count"])
        writer.writerows(outtweets)

    pass '''

def get_followings(username):
    user = api.get_user(username)
    following = []
    for friend in tweepy.Cursor(api.friends, screen_name=username).items():
        if friend.verified == True:
            following.append(friend.screen_name+" "+friend.name+" "+friend.description)
    if len(following)!=0:
        followings_classified = cla.get_followings_classified(following)
    else:
        followings_classified = [0, 0,0 ,0]
    print('master done')
    print(len(following))
    return user.name,user.location,user.friends_count,user.followers_count,user.statuses_count,user.created_at, followings_classified


if __name__ == '__main__':
    if check.is_connected() == True:
        get_all_tweets(username)
    else:
        print("check the internet connection!")
