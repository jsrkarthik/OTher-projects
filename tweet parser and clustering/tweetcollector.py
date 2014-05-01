import tweepy
import time
import sys
from random import randint
    
#Stuff used for authentica tion to twitter account
consumer_key = 'rcdbXbMyYAbaJ0DertwAjg'
consumer_secret = 'JHcX2LVxxRZb9zgJi7J9j8my2Rvu6OHYbKM6HFjUKBI'
access_key = '75150596-Y7hxPYCotMtrcBvXZ8sCsnGbLalgBBFJyS9PFDMR4'
access_secret = 'Hi9LstuYQxR4sgfMfPyH4bqxnBkjVK2SSehyCnj2VKWmF'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

while 1:
	i=0
	print "pls enter query.Press Q to quit"
	query=raw_input()
	if query=='Q':
	   break
	#twitter api.search api lets us to search in Twitter any query and results search results
	for tweet in api.search(q=query,count=50,		                  
		                    result_type="recent",
		                    include_entities=True,
		                    lang="en"):
	    if i < 50 :
	     print tweet.id,
	     print tweet.text
	     print "\n"
	    else:
	     break
	    i+=1
