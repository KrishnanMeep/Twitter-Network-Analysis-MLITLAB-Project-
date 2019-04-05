'''
Twitter API Code for the ML IT Lab Project
Group : 18MCMI03, 18MCMI04 and 18MCMI09
Pulls a certain number of tweets based on a topic/hashtag and then dumps all of it into csv files
'''

import tweepy
import json
import os
import pandas as pd

#Lookup tables
users2ID = {}
location2ID = {}
date2ID = {}


def PullTweets(query, prevId, file, t):
	results = api.search(query, lang = "en", count = 100, max_id = prevId - 1)
	tweets = []
	ParsedTweet = 0
	print(prevId, len(results))
	if len(results) == 0:
		print("No more tweets available")
		return -1
	
	for tweet in results:
		ParsedTweet = (tweet._json)
		userName =  ParsedTweet["user"]["name"]
		location = ParsedTweet["user"]["location"]
		date = ParsedTweet["created_at"][:10]

		if userName not in users2ID:
			users2ID[userName] = []
		users2ID[userName].append(ParsedTweet["id"])

		if location not in location2ID:
			location2ID[location] = []
		location2ID[location].append(ParsedTweet["id"])

		if date not in date2ID:
			date2ID[date] = []
		date2ID[date].append(ParsedTweet["id"])

		tweets.append(ParsedTweet)

	df = pd.DataFrame.from_dict(tweets)
	df.to_csv(file, mode='a', header=t, index=False)

	return int(ParsedTweet["id"])


if __name__ == '__main__':
	#Set of keys for twitter authentication
	consumer_key = "KA4EcNSW3zMc6V7s1EUGrW9BT"
	consumer_secret = "f1BXDBB1NQjHiEAPrnFmPnOUzLTUDUpyYn4gVREqpeZLha17z0"
	access_token = "3175602566-XPGiAEmA1Rz0iDI68DB3ekUWzdYzxgRR0ICNtZW"
	access_token_secret = "OlAqs0o1LnbDWVKW3MkudLiYuHU7vZQdqNi2YFvosfM2s"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	#This is where you put the term you want to search for
	query = "pikachu"
	file = "Pikachu.csv"
	if os.path.isfile(file):
		os.remove(file)

	lastId = api.search(query, lang = "en", count = 1)[0].id
	
	#Each pull gets a maximum of a hundred tweets, so 50 iterations is around 5000 tweets
	for i in range(50):
		lastId = PullTweets(query, lastId, file, not(i))
		print(lastId)
		if lastId == -1:
			break

	with open('users2ID'+query+'.json', 'w') as fp:
		json.dump(users2ID, fp)
	with open('location2ID'+query+'.json', 'w') as fp:
		json.dump(location2ID, fp)
	with open('date2ID'+query+'.json', 'w') as fp:
		json.dump(date2ID, fp)
