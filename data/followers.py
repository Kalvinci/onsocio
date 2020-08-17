import tweepy

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_followings(user_name):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth,  wait_on_rate_limit=True)
	user = api.get_user(user_name)
	print(user)
	#friend_ids = []
	#friend_bio = []
	#for friend in tweepy.Cursor(api.friends, screen_name = user_name).items():
	#	if friend.verified == True:
	#		friend_ids.append(friend.name)
	'''friend_ids = api.friends_ids(screen_name = user_name)
	print(friend_ids)
	for i in friend_ids:
		u = api.get_user(i)
		friend_bio.append(u.description)
	print(friend_bio)'''
	
get_followings('@akspthegoku')
