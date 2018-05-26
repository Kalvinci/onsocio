#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import pickle



#Twitter API credentials
consumer_key = "QJMv5JMtygcJP1b4mdiO0j7G6"
consumer_secret = "j2Kb1UXIiidhURgw3aTfcLyFWCIBQJrAd8XUEDDBn6Nw4vgqEB"
access_key = "2780669995-2utlBroP7o04duf0oR9C3MdbU28VzEWVtrS0Usc"
access_secret = "PAsP6iTlvul4EdBw8qKKeqE6OB0OP84BDRmp74HhqiMkS"


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth,  wait_on_rate_limit=True)

    #Fetching user information
    user = api.get_user(screen_name)
    print(user.name)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended')
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended', max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode('utf-8'),tweet.retweet_count,tweet.favorite_count] for tweet in alltweets]
    #write the csv    
    with open('%s_tweets.csv' % screen_name, 'w') as f: #replace w with 'a' for append mode.'kks' 
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text","retweet_count","favorite_count"]) #comment this line from the second time onwards. 'kks'
        writer.writerows(outtweets)
    
    pass

if __name__ == '__main__':
    #pass in the username of the account you want to download. 'kks'
    username = str("@satyammutha")
    get_all_tweets(username)