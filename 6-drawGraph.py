# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import networkx as nx
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import sys


myG = nx.DiGraph()

#we are taking as argument the tsv of the graph we want to analyse
#at the beginning you have only Email-Enron.txt but then you can create
#a tsv also from the graph created from twitter
path = str(sys.argv[1])
f = open(path, 'r')
read = csv.reader(f, delimiter='\t')

#Let's read this tsv and create our directed graph.
#Enron is that big that you probably want to take a subgraph.
#but that is not the case if you are using a tsv created from twitter
#Anyway if you do take a subgraph, you need to select the number of edges 
#you want to get among all the ones in the txt.
#To have something more random I decided to take some of the edges in the beginning and
#some of the edges randomly so it's not totally disconnected or totally connected
print 'Computing the whole graph from the txt will take time for Email-Enron.txt .'
print 'It will not take too much time for a graph from twitter.'
print 'Do you want to take just a part of the graph to spend less time? < y / n >'
yn = str(raw_input('-->'))
#if you decided to take a subgraph..
if yn == 'y':
	print 'How many edges do you want to get from the txt to create the graph?'
	print '5000 is advised for Email-Enron.txt'
	#stop is the number of edges you want in your subgraph
	stop = int(raw_input('-->'))
	print 'Creating graph..'
	countf = 0
	#let's take stop/5 edges from the first lines of the txt
	for row in read:
		#skipping comments
		if row[0][0] != '#':
			myG.add_edge(int(row[0]),int(row[1]))
			countf = countf + 1
		#let's stop when we get to stop/5 edges
		if countf == int(stop/5):
			break
	print 'The first', countf, 'edges have been added.'
	#now we will take random edges until we get around 4/5*stop random edges
	rnd = (stop*4/5) / float(367662)
	countr = 0
	for row in read:
		if random.random() < rnd:
			if row[0][0] != '#':
				myG.add_edge(int(row[0]),int(row[1]))
				countr = countr + 1
	print countr, 'random edges have been added.'
	
#if you didn't choose to do that mess and instead you want the full graph
#(highly advised for twitter graph)
elif yn == 'n':
	print 'Computing full graph..'
	count = 0
	#we just scroll the full file and take every edge
	for row in read:
		if row[0][0] != '#':
			myG.add_edge(int(row[0]),int(row[1]));
			count = count + 1
	print 'All',count, 'edges have been added.'
	if count == 0:
		sys.exit('ERROR: the graph is empty')
#please don't write anything different from y or n
else:
	sys.exit('ERROR: please type "y" or "n" next time') 

#if we are actually doing a twitter graph we can finally use 
#the txt printed from 2-tweets_id.py to have also labels
#with twitter names and number of followers
if path == 'graphTwitter.txt':
	print 'Retrieving infos about users from id_name_count.txt'
	f2 = open('id_name_count.txt','r')
	read = csv.reader(f2, delimiter = ',')
	User_id = []
	User_name = []
	User_count = []
	i = 0
	for row in read:
		if i != 0 :
			User_id.append(row[0])
			User_name.append(row[1])
			User_count.append(int(row[2]))
		i = i + 1
	#created dictionary used after for node labels
	Id_name = dict(zip(User_id,User_name))
	Id_count = dict(zip(User_id,User_count))
	


#we will use this to draw graphs
def drawGraph(G,namepng):
	plt.clf()
	plt.figure(figsize=(80,40))
	n = len(G.nodes())
	nodesDegree=G.degree()
	avgDeg = np.mean(nodesDegree.values())
	pos=nx.spring_layout(G)
	nx.draw(G,pos,node_color='b',node_size=10)
	dLabel = {}
	#what I do is to draw again each node so that I can set color and size by the node degree
	for x in G.nodes():
		d_x = nodesDegree[x]
		d_n = d_x/float(n)
		a = 50
		b = 100
		c = 400
		uno = (d_n*a)/(1+int(d_n*a))
		due = (d_n*b)/(1+int(d_n*b))
		tre = (d_n*c)/(1+int(d_n*c))
		
		nx.draw_networkx_nodes(G,
							   pos,
							   nodelist=[x],
							   node_size=d_x*500,
							   node_color=(uno, due, tre))
		#if the degree is high enough i'll write the label in the dictionary of labels
		if path == 'graphTwitter.txt': 
			if d_x >= max(nodesDegree.values())/float(2):
				try:
					dLabel[x] = Id_name[str(x)] + '- fol:' + str(Id_count[str(x)])
				except KeyError:
					continue
	#print labels in the dictionary in the figure	
	nx.draw_networkx_labels(G,pos,labels = dLabel,font_size = 24, font_color = 'r' )
	plt.savefig(namepng+'.png')
	plt.close()
	
print 'Drawing full graph..'	
drawGraph(myG,'full_graph')

undirMyG = nx.Graph(myG)

componenteList = list(nx.connected_component_subgraphs(undirMyG))

print 'Drawing largest component..'
drawGraph(componenteList[0],'largest_component')

coreResult = nx.k_core(componenteList[0])

print 'Drawing core of largest component..'
drawGraph(coreResult,'core_largest_component')

print 'Drawing medium component..'
if len(componenteList) > 1:
	drawGraph(componenteList[len(componenteList)/2],'medium_component')