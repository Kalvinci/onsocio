import tweepy

consumer_key = "QJMv5JMtygcJP1b4mdiO0j7G6"
consumer_secret = "j2Kb1UXIiidhURgw3aTfcLyFWCIBQJrAd8XUEDDBn6Nw4vgqEB"
access_key = "2780669995-2utlBroP7o04duf0oR9C3MdbU28VzEWVtrS0Usc"
access_secret = "PAsP6iTlvul4EdBw8qKKeqE6OB0OP84BDRmp74HhqiMkS"


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