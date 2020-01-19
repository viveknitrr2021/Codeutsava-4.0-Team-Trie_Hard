# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, render_template,request
import re 
import sys
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__,template_folder='',static_url_path='',static_folder='C:/Users/njhab/Desktop/ver/') 

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function. 

###File Operations###
# fileoperation=1
# if(fileoperation):
#     orig_stdout = sys.stdout
#     orig_stdin = sys.stdin
#     inputfile = open('W:/Competitive Programming/input.txt', 'r')
#     outputfile = open('W:/Competitive Programming/output.txt', 'w',encoding="utf-8")
#     sys.stdin = inputfile
#     sys.stdout = outputfile


class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''

		# keys and tokens from the Twitter Dev Console 
		consumer_key = '5EhfGyRXogUZ8xiivRjdMTFVn'
		consumer_secret = 'JKnBzM1SpFLsyqd0n6GL5o8n2XVwUSMwQP9F2t63SiflautfDg'
		access_token = '860202112159842304-KjgYShkWnGSEW26tbeUi95sxVieperi'
		access_token_secret = 'idGY6kPaT5ZHJuGdZYPgD8MHv9EKWYUiGbKzXZavcidQN'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 100000): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

@app.route('/') 


def hello_world(): 
	# creating object of TwitterClient Class 
	print("EXecuting...")
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = "ram mandir") 

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# picking neutral tweets from tweets 
	netweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 

	# printing first 5 positive tweets 
	# print("\n\nPositive tweets:") 
	# for tweet in ptweets[:10]: 
	# 	print(tweet['text']) 

	# # printing first 5 negative tweets 
	# print("\n\nNegative tweets:") 
	# for tweet in ntweets[:10]: 
	# 	print(tweet['text']) 

	# # printing first 5 neutral tweets 
	# print("\n\nNeutral tweets:") 
	# for tweet in netweets[:10]: 
	# 	print(tweet['text'])
	print(tweets)
	return render_template('index.html',context={"tweets":tweets})
# main driver function 
if __name__ == '__main__': 

	# run() method of Flask class runs the application 
	# on the local development server. 
	app.run(port=8000) 
