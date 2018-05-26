import pandas as pd
import pickle
user="@amritbhat907"
tweet = pd.read_csv('App_Data/%s_tweets.csv'%(user))
tweet = tweet['text']
print("%s"%(tweet))