import tweepy
import json
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict


def PullTweets( query, prevId, file, t ):
	results = api.search(query, lang = "en", count = 10, max_id = prevId - 1)
	tweets = []
	for tweet in results:
		ParsedTweet = (tweet._json)
		for nested in ["entities", "user", "retweeted_status"]:
			for key, value in zip(ParsedTweet[nested].keys(), ParsedTweet[nested].values()):
				ParsedTweet[str(nested) + "." + str(key)] = value
			del ParsedTweet[nested]
		tweets.append(ParsedTweet)

	df = pd.DataFrame.from_dict(tweets)
	print(df.columns)

	df.to_csv(file, mode='a', header=t, index=False)
	return int(ParsedTweet["id"])


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
	
	for i in range(1):
		lastId = PullTweets( query, lastId, file, not(i))
