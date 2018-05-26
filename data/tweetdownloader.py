import pickle
import os

if not os.path.exists('secret_twitter_credentials.pkl'):
    Twitter={}
    Twitter['Consumer Key'] = 'QJMv5JMtygcJP1b4mdiO0j7G6'
    Twitter['Consumer Secret'] = 'j2Kb1UXIiidhURgw3aTfcLyFWCIBQJrAd8XUEDDBn6Nw4vgqEB'
    Twitter['Access Token'] = '2780669995-2utlBroP7o04duf0oR9C3MdbU28VzEWVtrS0Usc'
    Twitter['Access Token Secret'] = 'PAsP6iTlvul4EdBw8qKKeqE6OB0OP84BDRmp74HhqiMkS'
    
import tweepy

auth = twitter.oauth.OAuth(Twitter['Access Token'],
                           Twitter['Access Token Secret'],
                           Twitter['Consumer Key'],
                           Twitter['Consumer Secret'])

twitter_api = twitter.API(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print(twitter_api)

texts = twitter_api.GetUserTimeline(screen_name='@amritbhat907')
print(texts)