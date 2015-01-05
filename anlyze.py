#!/bin/env python
from senti_classifier import senti_classifier
sentences = ['The movie was the worst movie', 'It was the worst acting by the actors']
pos_score, neg_score = senti_classifier.polarity_scores(sentences)
print pos_score, neg_score
''''
#!/bin/env python
import requests, json, urllib, sys , logging, os, time
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from requests_oauthlib import OAuth1

import urllib
import urllib2

CONSUMER_KEY = "D1847mqj9wX1r0Dz0LJgVouG2"
CONSUMER_SECRET = "ZnAAJupzllq5nawLG2lekSSAPOzqcSNiGdykIZTVKaz7efYzPr"
ACCESS_KEY = "2289227376-fYVHTyoLIbtYs3eCMRseUiwrN0zTfJhv7k3UhUR"
ACCESS_SECRET = "J96DyJjSAcqPxK1AGZMtEcA9VzGZgl9jKd3p0SOR6NEDQ"

def log_error(error):
	try:
		logging.basicConfig(filename='error.log' , format='%(asctime)s %(levelname)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
		logging.error(error)
	except IOError as e:
		email_error("I/O error({0}): {1}".format(e.errno, e.strerror) + error)
	except:
		email_error("Unknown error occurred at log_error. " + sys.exc_info()[0] + error)
		
def save_last_tweet_id(tweet_id):
	try:
		file = open('last_tweet' , 'w')
		file.write(str(tweet_id) + '\n')
		file.close()
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at save_top_story. " + sys.exc_info()[0])

def read_last_tweet_id():
	try:
		if os.path.exists('last_tweet'):
			file = open('last_tweet' , 'r')
			last_top_story = file.readline()
			if last_top_story == "":
				last_top_story = 0
			file.close()
		else:
			last_top_story = 0
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at read_last_top_story. " + sys.exc_info()[0])
	return last_top_story

def get_tweets():
	url = 'https://api.twitter.com/1.1/search/tweets.json'
	auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
	last_tweet_id = read_last_tweet_id()
	if last_tweet_id == 0:
		payload = {'q': '#PresPollSL', 'count': 100 }
	else:
		last_tweet_id = int(last_tweet_id)
		payload = {'q': '#PresPollSL', 'count': 100, 'since_id': last_tweet_id }
	response = requests.get(url, auth=auth, params=payload)
	return json.loads(response.text), last_tweet_id

def print_result(count, overall, positive, negative, neutral):
	print "**********************************************"
	print "***************Analysis Result****************"
	print "**********************************************"
	print "Analysed %d tweets." % (count - 1) 
	print "Compound Status:\t %.2f" % overall
	print "Neutral Sentiment:\t %.2f" % neutral
	print "Positive Sentiment:\t %.2f" % positive
	print "Negative Sentiment:\t %.2f" % negative
	print "**********************************************"
	
def main():
	text = ""
	count = 1
	tweets, last_tweet_id = get_tweets()
	if tweets['statuses']:
		for tweet in tweets['statuses']:
			if is_ascii(tweet['text']):
				print str(count) + "\t: " + tweet['text'] + "\n"
				count = count + 1
				text = text + tweet['text']
			if last_tweet_id < int(tweet['id']):
				last_tweet_id = int(tweet['id'])
		overall, positive, negative, neutral = analyze(text)
		print_result(count, overall, positive, negative, neutral)
		save_last_tweet_id(last_tweet_id)
	else:
		print "No new Tweets..."

def is_ascii(text):
	try:
		text.decode('ascii')
	except:
		return False
	return True
	
def analyze(text):
	result = vaderSentiment(text)
	print result
	return result['compound'], result['pos'], result['neg'], result['neu']

main()'''