import tweepy
import json
import os
import pandas as pd
from datetime import datetime


def PullTweets( query, prevId, file, t ):
	results = api.search(query, lang = "en", count = 100, max_id = prevId - 1)
	tweets = []
	for tweet in results:
		tweets.append([tweet.id, tweet.user.screen_name, datetime.strftime(tweet.created_at, "%d, %H:%M:%S")])

	df = pd.DataFrame(tweets, columns = ['ID', 'User', 'Time'])
	print(df)
	df.to_csv(file, mode='a', header=t, index=False)
	return tweets[-1][0]


if __name__ == '__main__':
	#Set of keys for twitter authentication
	consumer_key = "#"
	consumer_secret = "#"
	access_token = "#"
	access_token_secret = "#"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	query = "tech breakup"
	file = "TechBreakup.csv"
	if os.path.isfile(file):
		os.remove(file)

	lastId = api.search(query, lang = "en", count = 1)[0].id
	
	for i in range(175):
		lastId = PullTweets( query, lastId, file, not(i))
