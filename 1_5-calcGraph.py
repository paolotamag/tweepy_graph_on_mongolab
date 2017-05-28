# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import networkx as nx
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import sys


theStart = time.time()
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
#please don't write anything different from y or n
else:
	sys.exit('ERROR: please type "y" or "n" next time') 
		


print 'Computing degree..'
dizDeg = myG.degree()
degreeOfNodes = sorted(dizDeg.values(),reverse=True)

print 'Plotting degree distribution..'
plt.figure(figsize=(20,10))
plt.loglog()

plt.plot(degreeOfNodes, 'o') 

plt.ylabel('log(Degree)')
plt.xlabel('log(Number of nodes)')
plt.savefig("Degree_Distrib.png")
plt.close()

#to do certain operation we need to have an undirected graph
#no big deal we'll convert our directed one
undirMyG = nx.Graph(myG)

print 'Computing clustering coeff...'

import collections
dizClust = nx.clustering(undirMyG)
#here I had to play a bit with the dictionary of the clust. coeff.
#so I could print interesting values of clust coeff and not just 0 or 1 that in some case
#is really frequent and you cannot just pick randomly nodes to get different values 
dizClust = collections.OrderedDict(sorted(dizClust.items()))
kess = dizClust.keys()
vals = dizClust.values()

intrestingValue = sorted(set(vals))[len(sorted(set(vals)))/4]
keyOfIntr = kess[vals.index(intrestingValue)]
print 'the clustering coeff. of node', keyOfIntr, 'is', nx.clustering(undirMyG, keyOfIntr)

intrestingValue = sorted(set(vals))[len(sorted(set(vals)))/2]
keyOfIntr = kess[vals.index(intrestingValue)]
print 'the clustering coeff. of node', keyOfIntr, 'is', nx.clustering(undirMyG, keyOfIntr)

intrestingValue = sorted(set(vals))[len(sorted(set(vals)))*3/4]
keyOfIntr = kess[vals.index(intrestingValue)]
print 'the clustering coeff. of node', keyOfIntr, 'is', nx.clustering(undirMyG, keyOfIntr)

intrestingValue = min(vals)
keyOfIntr = kess[vals.index(intrestingValue)]
print 'the clustering coeff. of node', keyOfIntr, 'is', nx.clustering(undirMyG, keyOfIntr)

intrestingValue = max(vals)
keyOfIntr = kess[vals.index(intrestingValue)]
print 'the clustering coeff. of node', keyOfIntr, 'is', nx.clustering(undirMyG, keyOfIntr)

print 'the average clustering coeff. of the graph is', np.mean(dizClust.values())

print 'Computing components..'
componenteList = list(nx.connected_component_subgraphs(undirMyG))

#if the graph is full connected:
if len(componenteList) == 1:
	print 'Only one component has been found'
	print 'The graph is full connected!'
#otherwise let's prit the number of components
else:
	print len(componenteList), 'components have been found'

print 'The full graph has',len(myG.nodes()),'nodes.' 
#the largest component is the first in the list because that list is sorted in a 
#decreasing order of number of nodes
print 'The largest component has',len(componenteList[0].nodes()),'nodes.'
	
print 'Computing k-core on largest component..'
coreResult = nx.k_core(componenteList[0])

print 'Computing indegree centrality..'
dizDegIn = nx.in_degree_centrality(myG)
degreeOfNodesIn = sorted(dizDegIn.values(),reverse=True)

	
print 'Computing outdegree centrality..'
dizDegOut = nx.out_degree_centrality(myG)
degreeOfNodesOut = sorted(dizDegOut.values(),reverse=True)

#this will take time
print 'Computing closeness centrality..'
dizClose = nx.closeness_centrality(myG)
closeOfNodes = sorted(dizClose.values(),reverse=True)

#this even more time
print 'Computing betweenness centrality..'
dizBet = nx.betweenness_centrality(myG)
betOfNodes = sorted(dizBet.values(),reverse=True)


print 'Computing pagerank..'
dizPg = nx.pagerank(myG)
PgOfNodes = sorted(dizPg.values(),reverse=True)

	
#but if you do wait you'll see a nice plot of all the properties distribution
print 'Plotting all the distributions..'
plt.figure(figsize=(20,10))
plt.loglog()
plt.plot(degreeOfNodesIn,'o-') 
plt.plot(degreeOfNodesOut,'o-') 
plt.plot(closeOfNodes,'o-') 
plt.plot(betOfNodes,'o-') 
plt.plot(PgOfNodes,'o-') 

plt.legend(['Indegree', 'Outdegree', 'Closeness','Betweness', 'Pagerank'])
plt.ylabel('log(Property)')
plt.xlabel('log(Number of nodes)')
plt.savefig("deg_close_bet_pg.png")
plt.close()

theEnd = time.time()
print 'Elapsed time:',int(theEnd - theStart)/60, 'm,', int(theEnd - theStart)%60,'s'