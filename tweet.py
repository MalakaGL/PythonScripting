#!/bin/env python
import requests, json, sys , logging, os, time
from datetime import datetime
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from requests_oauthlib import OAuth1
from pymongo import MongoClient

CONSUMER_KEY = "D1847mqj9wX1r0Dz0LJgVouG2"
CONSUMER_SECRET = "ZnAAJupzllq5nawLG2lekSSAPOzqcSNiGdykIZTVKaz7efYzPr"
ACCESS_KEY = "2289227376-fYVHTyoLIbtYs3eCMRseUiwrN0zTfJhv7k3UhUR"
ACCESS_SECRET = "J96DyJjSAcqPxK1AGZMtEcA9VzGZgl9jKd3p0SOR6NEDQ"

def log_error(error):
	try:
		logging.basicConfig(filename='error.log' , format='%(asctime)s %(levelname)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
		logging.error(error)
	except:
		sys.exit(1)

def save_last_tweet_id(connection, tweet_id):
	last_tweet = {'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'tweet_id':tweet_id}
	collection = connection.twitter.last_tweet_id
	collection.insert(last_tweet)

def read_last_tweet_id(connection):
	collection = connection.twitter.last_tweet_id
	tweet = collection.find().sort( [('_id',-1)] )
	if tweet:
		tweet_list = list(tweet)
		if tweet_list and tweet_list[0]['tweet_id']:
			return tweet_list[0]['tweet_id']
		else:
			return 0

def get_tweets(connection):
	url = 'https://api.twitter.com/1.1/search/tweets.json'
	auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
	last_tweet_id = read_last_tweet_id(connection)
	if last_tweet_id == 0:
		payload = {'q': '#PresPollSL', 'count': 200 }
	else:
		last_tweet_id = int(last_tweet_id)
		payload = {'q': '#PresPollSL', 'count': 200, 'since_id': last_tweet_id }
	response = requests.get(url, auth=auth, params=payload)
	return json.loads(response.text), last_tweet_id

def save_result(connection, text, overall, positive, negative, neutral):
	tweet = {'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'tweet':text,'overall':overall,'positive':positive,'negative':negative,'neutral':neutral}
	collection = connection.twitter.tweets
	collection.insert(tweet)

def open_db_connection():
	connection = MongoClient("mongodb://allion:allion123@ds029821.mongolab.com:29821/twitter")
	return connection

def main():
	text = ""
	count = 1
	connection = open_db_connection()
	tweets, last_tweet_id = get_tweets(connection)
	while tweets['statuses']:
		for tweet in tweets['statuses']:
			if is_ascii(tweet['text']):
				print str(count) + "\t: " + tweet['text'] + "\n"
				count = count + 1
				text = tweet['text']
				overall, positive, negative, neutral = analyze(text)
				save_result(connection, text, overall, positive, negative, neutral)
			if last_tweet_id < int(tweet['id']):
				last_tweet_id = int(tweet['id'])
		save_last_tweet_id(connection, last_tweet_id)
		tweets, last_tweet_id = get_tweets(connection)
	connection.close()

def is_ascii(text):
	try:
		text.decode('ascii')
	except:
		return False
	return True

def analyze(text):
	result = vaderSentiment(text)
	return result['compound'], result['pos'], result['neg'], result['neu']

main()