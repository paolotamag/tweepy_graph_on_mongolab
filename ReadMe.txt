Paolo Tamagnini - 1536242
Data Science - Algorithmic Methods of Data Mining
Academic year 2015–2016 - December 21th 2015

Project 2

I used a MongoDB on my computer instead of using MongoLab for storage memory problems.
I also used many tokens of Twitter to do a faster download, but I left here just one token in token.txt
The codes are highly commented but I'll explain what to do here too.

	1) Analysing the graph contained in Email-Enron.txt

	python 1_5-calcGraph.py Email-Enron.txt

	NetworkX is really slow to compute closeness and betweenes.
	You can take a subgraph of the huge graph by entering 'y' and typing the number of edge you want to get
	5000 is big enough and it won't take too long.
	The script will compute everything that is requested giving as output:
		- a plot of the  degree distribution
		- a print of the clustering coefficient of some nodes
		- a print of the number of components found
		- a print of the average clustering coefficient
		- a print of the number of nodes of the full graph and of the largest component
		- a plot containing the distributions for: indegree, outdegree, closeness, betweenes and pagerank


	2) Downloading 10'000 tweets with the query: 'Star Wars'
	
	python 2-tweets_id.py

	the script will download with 1 token 10k tweets containing the string 'Star Wars', exluding:
		- retweets
		- tweet of user with more than 1 million followers
		- tweet of protected users
	
	Each tweet will be uploaded in a dictionary like this one:

	{ '_id' = 'tweet id', 'text': 'tweet content', 'author': 'id of user who twitted'}

	I set as unique field the tweet id.

	The tweets will be uploaded on MongoDB in the collection 'tweets_Star_Wars'.
 
	To decide which database you want to choose you have 3 different options:

		a) on a NOT empty sandbox database on MongoLab called 'adm_prof_test'
		(it already has 500 tweets and all the followers of their 487 users)

		b) on a empty sandbox database on MongoLab called 'adm_prof_test'
		
		c) on your localhost database
	
	Check the screenshot of the dbs in the db_screenshot folder.
	To choose a database go in the script and remove the '#' from the line of the 'MONGODB_URI' you want.

	You can decide how many tweers you want to download for test purposes by typing the number of desired tweets.

	With 1 token is possible to download even more than 10k tweets so I don't have an exception here for tweepy.RateLimitError.
	It might happen such error if you used that token recently.

	If you want to try the script of 2-tweets_id.py choose option b) so you don't mess with the a) database,
	that is ready to create and draw a graph.

	In fact the script will output id_name_count.txt that contains info only needed later on for drawing a label over nodes.
	Unfortunately if you add more tweets to the database you will override the present file id_name_count.txt in the folder.
	Such file is relative to 500 tweets already in the database. If you add more tweets, labels won't show up in the end but 6-drawGraph.py
	will still run with no error. If you want to have labels even adding more tweets you need to erase first both collection from database,
	so it's better you just pick database b) instead.


	3) Downloading followers of the users who twitted the 10k tweets

	python 3-fol_id.py
	
	This script was supposed to run once for every token in token.txt each time with a different parameter as argument in the command line.
	I set the parameter to 0 so you don't need to worry about it and you run it only once with the only token you have in token.txt.
	The parameter was also used to split the list of users who twitted in many different list of same amount of element one for each token.
	The main concept was that by splitting this huge list of author-users in smaller and equal size list, each token could download
	an individual list while all the others were doing the same. The splitting is all automatic so even if you change the token.txt adding a new token,
	the script will adapt. There are screenshots in the folder output\parallel_work-fol_id so you can see how I ran the whole thing on Windows. 
	Anyway even with just one token it all works: parameter 'a' is 0 and number of tokens is 1 so it won't split and it will just start 
	the long download with just 1 token.
	
	First thing it will download a list of all the user who twitted from the collection 'tweets_Star_Wars'
	removing duplicates (user who twitted more than once with that query).

	If you want to try the code you should select first the database you want like in point 2) and the database b) is advised here as well
	(only if you already downloaded few tweets in part 2) with database b), otherwise it won't find any user to download).

	Each list of followers will be uploaded in a dictionary like this one: { '_id': 'id user who twitted', 'followers': [ ids of followers ]}
	This time I customized the unique field to be the id of the user who twitted.

	The entries are going to be insert in the collection 'followers_Star_Wars'.
	The limit of twitter is handled so that it retries every minute until the 15 minutes are passed (waiting 15 minutes was disconnecting me).
	Even if I got rid of protected users I got one or two users where I am not authorized for downloading the followers.
	I think it's about suspended twitter accounts and I handle the error 'Not authorized.' by skipping them. 
	Even if their entry will be in the collection, their followers list will be empty.
	Because of interruption of downloads and other issues I also managed how to retry the code without deleting the collection.
	I could do it cause I was able to skip downloading the followers of the ones already in the collection, so that it was going directly to the ones missing.



	4) Creating the graph from the data on MongoDB

	python 4-graphTwit.py

	This will generate a graph from the 2 collections on MongoDB. 

	You need to select the database here as well, like point 2) and 3).
	To find enough data to build a graph not empty you should select database a).

	It can also compute a subgraph just by scrolling a certain number of entries 
	of your choice from the colletcion 'followers_Star_Wars'. You just need to answer on command line at each question like for point 1).
	It will tell you how many are in the collection, how many different users who twitted and so on.

	The script will download first all the user who twitted from the collection 'tweets_Star_Wars' like in point 3)
	The script will then scroll the collection 'followers_Star_Wars' and for each entry it will scroll its list of followers and 
	add an edge from the follower to the user who twitted if the follower is himself in the list of the users who twitted. 
	By creating an edge between unexisting nodes, the nodes will be added. 
	This way the users who twitted, not connected to any others, will not be in the graph.
	The script will then output a TSV like the Email-Enron.txt listing all the edges as graphTwitter.txt

	
	5) Analysing the graph contained in graphTwitter.txt

	python 1_5-calcGraph.py graphTwitter.txt

	This point is like point 1) but with a different graph, our graph generated from twitter.
	The graph will not be that big in any case, so just type 'n' when it's asking to take a subgraph.

	
	6) Drawing the whole graph, its largest and medium components and the core of its largest component.

		A) python 6-drawGraph.py graphTwitter.txt
	
			OR

		B) python 6-drawGraph.py Email-Enron.txt

	It will define a function that draws a graph changing the nodes color and size by their degree.

	If you typed A) it will also get id_name_count.txt to draw the label to a node big enough.
	If you did A) and the file id_name_count.txt is missing it will raise error.
	If it is not missing but it is not the right one for your graphTwitter.txt,
	it won't raise error but it won't show many labels.
	If you want to try the code and see labels work properly either:
 
		- create graphTwitter.txt from point 4) on database a) and use just the id_name_count.txt in the folder "a)db_backUpLabels". 
		If database a) wasn't changed by adding new tweets or list of followers, there should be no problem.

		- or just go in the folder "a)db_backUpLabels" and run everything in there. This also will work just if 
		database a) wasn't changed by adding new tweets or list of followers.

	Also here you can decide if you want to take a subgraph or not.
	Take a subgraph if you did B), don't if you did A).


I succesfully downloaded all the followers of all the users who twitted that 10k tweets, maybe it wasn't needed but 
I took it as a challenge downloading over and over again.
MongoLab was giving 'quota exceeded errors' when I was far from the free cap of 500 mb because of some issue regarding journal files (http://goo.gl/qPFrKU).

So I forced myself to go on localHost and the only way I can show you is by attaching huge json files. 
(The tweets_Star_Wars.json file has an automatic unique field at each entry cause back then I was still doing like that)

I had 8451 different and not protected users with less than 1 million followers who tweeted the 10k tweets, 
and I was able to download all their followers except of one guy with suspended account.
I'm pretty happy about that and I actually enjoyed it.
In 'output\fullGraph_10k_tweets_StarWars\play_with_full_graph' you can use the TSV of this full graph to actually enjoy it yourself by
drawing and analysing the graph.


please let me know for any incomprehension

Paolo Tamagnini
paolotamag@gmail.com