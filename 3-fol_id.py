# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import tweepy
from tweepy import OAuthHandler
import time
import csv
from time import strftime
import sys
import pymongo

#this file python was supposed to run once for every token by taking as second argument
#a paramater that was telling him which token to use and which part of the list UserWhoTwitted
#to take in the search of followers. In the correction you are able to use just 1 token.
#So you can't see how the parameter splits the list and take 1/lenTok of the list elements.
#In here a = 0 and lenTok = 1 list used => UserWhoTwitted[0:]
a = 0
#a = int(sys.argv[1])
print 'Make sure you removed "#" from the line of the MONGODB_URI you want.'
time.sleep(5)

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


#creating auth for each token
oauthKey = zip(consKey,consSec,accTok,accTokSec)
Auths = []  
for consumer_key, consumer_secret, access_key, access_secret in oauthKey:  
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
    auth.set_access_token(access_key, access_secret)  
    Auths.append(auth)
lenTok = len(Auths)

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


#getting full list of users who twitted the 10k tweets
#by scrolling monogoDB cursor of all entries in 'tweets_Star_Wars' collection

tw = db['tweets_Star_Wars']
UserWhoTwitted = []
for x in tw.find():
    UserWhoTwitted.append(x['author'])
	
#getting rid of doubles (users who twitted more than once with that query are repeated)
# and sorting
UserWhoTwitted = sorted(set(UserWhoTwitted))
print 'Ho',len(UserWhoTwitted),'utenti diversi'

#defining how many users to give to each token depending on how many tokens I have
numUtperPy = len(UserWhoTwitted)/lenTok #OUR CASE: numUtperPy = len(UserWhoTwitted) / 1

#if I am using the last token just get all the remaining starting from the second last piece
#this is actually our case were we are using the first and last token of our list (the only token we have)
if a == (lenTok - 1):
	UserWhoTwitted = UserWhoTwitted[(numUtperPy*a):]
#otherwise just take the piece of list relative to our token (second token --> second piece)
else:
	UserWhoTwitted = UserWhoTwitted[(numUtperPy*a):(numUtperPy*(a+1))]
#defining method to take breaks when twitter stops me
def limit_handled(cursor):
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			print 'Waiting..'
			#printing the time so I could know what was going on
			print strftime("%Y-%m-%d %H:%M:%S"), 'Doing user:',x
			#I'll retry every minute otherwise twitter was stopping my connection
			#if i was waiting too long to retry
			time.sleep(1 * 60)
		#unfortunately even if we don't have protected account
		#we could meet other kind of account like suspended ones
		#in that case we are going to get the 'not authorized error'
		#if that happens we just skip him and we go to the next account
		except tweepy.error.TweepError as e:
			s = str(e)
			if s=='Not authorized.':
				print 'Unexpected suspended account'
				break
			else:
				print 'Unexpected error', s
#using a-th auth in Auths list
#that means using a-th token
api = tweepy.API(Auths[a])
#creating collection for the followers
fol = db['followers_Star_Wars']
#for each user who twitted that I have to do with this token
for x in UserWhoTwitted:
	print 'Doing Followers of', x
	print 'using key', a
	#create a dictionary
	d = {}
	#with mongoDB primary key = to the user id
	d['_id'] = x
	#if you are doing many parallel retries you can but 
	#you need to check to not insert anything that was already 
	#inserted in the collection, to do so you just check a query counting how many
	#entries you got with such _id. If you don't you'll get anyway a pymongo.errors.DuplicateKeyError
	#that you can handle but just after downloading a user you already have, cause the error
	#comes up just after when you insert the dictionary, and you would waste so many twitter calls
	#for user you already had..
	if fol.count(d)!= 0:
		print 'Skipping',x,'to avoid duplicate without wasting twitter calls'
		continue
	#create a cursor that scrolls the follower id of the user
	cursor = tweepy.Cursor(api.followers_ids, user_id=x)
	p = 0
	#create empty list where we will append his followers
	FollOfGuy = []
	for result in limit_handled(cursor.pages()):
		p = p + 1
		#for each page in the cursor let's scroll the followers id 
		for y in result:
			#appending each of them in the list
			FollOfGuy.append(y)
		print 'pagina', p
	#in the end of each user cycle let's insert the list in the dictionary
	print 'Adding new entry..'
	d['followers'] = FollOfGuy
	#and then let's insert the dictionary on mongolab collection
	#trying to see if we already had such dictionary..
	#this error should never happen cause we already check before counting 
	#the number of entries with this id, so it is just an extra check	
	try: 
		fol.insert(d)
	except pymongo.errors.DuplicateKeyError:
		print 'Skipping',x,'to avoid duplicate after wasting twitter calls'
		continue




