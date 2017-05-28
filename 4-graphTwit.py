# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
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

import sys
import pymongo
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

#honestly if you run this on command line you'll see better what happens
#but you need some tweet and followers list on that database so run the others previously
#I give the choice to also just create a subgraph that reads a number 
#of your choice of entries of the followers collection

print "It's time to create the graph from the twitter info on MongoDB."
print "The graph will comprehend just the nodes relative to twitter accounts"
print "who twitted our query and which are connected to at least another account"
print "who twitted that same query."
print "Computing the whole graph will take long.." 
print "Do you want to take a subgraph? < y / n >"
print 'Make sure you removed "#" from the line of the MONGODB_URI you want.'
yn = raw_input('-->')

nb = 10000
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
tw = db['tweets_Star_Wars']
fol = db['followers_Star_Wars']

#getting full list of users who twitted the 10k tweets
#by scrolling monogoDB cursor of all entries in 'tweets_Star_Wars' collection
print 'Getting list of users who twitted..'
UserWhoTwitted = []
for x in tw.find():
    UserWhoTwitted.append(x['author'])
UserWhoTwitted = sorted(set(UserWhoTwitted))
nUwT = len(UserWhoTwitted)

print 'In the collection "tweets_Star_Wars" are present',nUwT,'different users who twitted.'
print 'In the collection "followers_Star_Wars" were uploaded just',fol.count(),'of them.'

if yn == 'y':
	print 'How many user who twitted do you want to check in the "followers_Star_Wars" collection?'
	print 'The max you can get is',fol.count(),'.'
	nb = int(raw_input('-->'))
elif yn !='y' and yn !='n':
	sys.exit('ERROR: please type "y" or "n" next time')


if yn == 'y':
	print 'Checking if they are within the followers of'
	print 'the first', nb, 'users in "followers_Star_Wars" collection.'
else:
	print 'Checking if they are within the followers of the same users'
	print 'within the "followers_Star_Wars" collection.'
	
time.sleep(4) #a little extra time to read better


print 'Creating graph..'
time.sleep(2)
#creating directed graph
justUsers = nx.DiGraph()
count = 0
#for each entry in 'followers_Star_Wars'
for x in fol.find():
	count += 1
	#defining name of node
	Id = x['_id']
	print 'Doing user #',count,':', Id
	#if you had this also user who twitted not connected 
	#to any other user who twitted are going to be present:
	#justUsers.add_node(Id)
	
	#for each follower of x
	for y in x['followers']:
		#if it is also a user who twitted one of the 10k tweets
		if y in UserWhoTwitted:
			print 'Found user',y, 'in followers of',Id
			#add an edge between him and x
			justUsers.add_edge(y,Id)
	if yn == 'y':
		if count == nb:
			break
if len(justUsers.nodes())==0:
	print 'The graph is empty cause no match has been found.'
#once we are done creating the graph it is nedded
#to output a TSV txt file looking exactly as the Email-Enron.txt
print 'Creating tsv listing all the edges..'
file = open('graphTwitter.txt', 'w')
writer = csv.writer(file, delimiter='\t')
for x in justUsers.edges():
	writer.writerow(x)