# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import tweepy
from tweepy import OAuthHandler
import time
import csv
from time import strftime
import sys
import pymongo
import pandas as pd
nt = 10*4
print 'How many tweets do you want to download?'
print "It should be 10'000 tweets, but it takes long and I want you to decide."
print 'Make sure you removed "#" from the line of the MONGODB_URI you want.'
nt = int(raw_input('-->'))
#GETTING TOKENS FROM TXT
f = open('token.txt', 'r')
read = csv.reader(f, delimiter=',')
consKey = []
consSec = []
accTok = []
accTokSec = []
for row in read:
    consKey.append(row[0].replace("'", ""))
    consSec.append(row[1].replace("'", ""))
    accTok.append(row[2].replace("'", ""))
    accTokSec.append(row[3].replace("'", ""))
lenTok = len(consKey)
#creating auth for each token
oauthKey = zip(consKey,consSec,accTok,accTokSec)
Auths = []  
for consumer_key, consumer_secret, access_key, access_secret in oauthKey:  
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
    auth.set_access_token(access_key, access_secret)  
    Auths.append(auth)


#using first auth
api = tweepy.API(Auths[0])

#creating cursor with query 'Star Wars' without retweets
cursor = tweepy.Cursor(api.search, q ='Star Wars'+"-filter:retweets",count=100, lang="en")

#connecting to mongolab database created for you to try the code

__author__ = 'mongolab'

#plese select your database

#a)DATABASE WITH 500 TWEETS AND ALL OF THE FOLLOWERS OF THE 487 USERS WHO TWITTED
#use this to create a graph
#MONGODB_URI = 'mongodb://root:root@ds033875.mongolab.com:33875/adm_prof_test'

#b)EMPTY DATABASE
#use this to download more tweets and more followers
#MONGODB_URI = 'mongodb://root:root@ds033915.mongolab.com:33915/adm_prof_test'

#c)LOCAL HOST
#MONGODB_URI = 'mongodb://localhost:27017/StarWarstwit'

client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()

#creating collection of tweets on mongolab
tweets = db['tweets_Star_Wars']
count = 0
c = 0
Uwt_id = []
UwT_screen_name = []
UwT_followers_count = []
for result in cursor.pages():
	count = count + 1
	print 'page', count
	for x in result:
		print 'tweet',c
		#for each tweet in the query result I'll check if the user has less than 1M followers and if it is protected or not
		if(x.author.followers_count <= 10**6 and x.author.protected == False):
			#if it's not too famous and not protected I'll save in memory his
			#id
			Uwt_id.append(x.author.id)
			#twitter name
			UwT_screen_name.append(x.author.screen_name)
			#the number of his followers
			UwT_followers_count.append(x.author.followers_count)
			#and I'll insert the tweet text and his author id on mongolab
			d = {}
			d['_id'] = x.id
			d['text'] = x.text.encode('utf-8')
			d['author'] = x.author.id
			tweets.insert(d)
			c = c + 1
		else:
			print 'User not added:', x.author.screen_name, x.author.followers_count, 'Protected:', x.author.protected
		#I'll stop when I hit 10k tweets
		if c == nt:
			break
	if c == nt:
		break
#just for drawing purposes I'll save the id the twitter name and the number of followers in a csv
UwT = pd.DataFrame()
UwT['id'] = Uwt_id
UwT['screen_name'] = UwT_screen_name
UwT['followers_count'] = UwT_followers_count

UwT.to_csv('id_name_count.txt',index = False)