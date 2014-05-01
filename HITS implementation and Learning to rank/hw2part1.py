import cjson
import numpy
import collections
import math
from operator import itemgetter
import networkx as nx
import os
import re
srcdir='./homework2 files'
for path, dirs, files in os.walk(srcdir):
    for filename in files:
         if filename=='tweets.txt':
            f=open(path+'/'+filename)
count = 0
#using DiGraph for graph construction
DG=nx.DiGraph()
# preprocessing the JSON file using cjson library and saving the information in the Graph as nodes and edges as described in the homework
for line in f:	
    data = cjson.decode(line)
    if not DG.has_node(data['user']['screen_name']):        
        DG.add_node(data['user']['screen_name'],hubscore=1,authscore=1)
        
    i=0     
    while i < len(data['entities']['user_mentions']):
       if not DG.has_node(data['entities']['user_mentions'][i]['screen_name']):
           DG.add_node(data['entities']['user_mentions'][i]['screen_name'],hubscore=1.0,authscore=1.0)
           #print data['entities']['user_mentions'][i]['screen_name']
       if not DG.has_edge(data['user']['screen_name'],data['entities']['user_mentions'][i]['screen_name']):
           DG.add_edge(data['user']['screen_name'],data['entities']['user_mentions'][i]['screen_name'],weight=1)
       i+=1
#obtaining all the  weakly connected component subgraph
sub_graphs = nx.weakly_connected_component_subgraphs(DG)
maxx=0
maxsg=0
#obtaining the largest one among all
for i, sg in enumerate(sub_graphs):
    if sg.number_of_nodes()>maxx:
       maxx=sg.number_of_nodes()
       maxsg=i    
SG=sub_graphs[maxsg]
j=0
# found that until 587 iterations values are converging. Found the value of 587 by experimentation with different number of iterations and convergence
#computing the Hub score and authority score according to HITS Algorithm 
while j < 622:

 temp=nx.DiGraph()
 temp=SG
 for node in temp.nodes():
    for pred in temp.predecessors(node):
        temp.node[node]['authscore']+=temp.node[pred]['hubscore']
 for node in SG.nodes():
    for succ in SG.successors(node):
        SG.node[node]['hubscore']+=SG.node[succ]['authscore']
 SG=temp       
 sumauth=0
 sumhub=0
 for node in SG.nodes():
      sumauth+=SG.node[node]['authscore']*SG.node[node]['authscore']
      sumhub+=SG.node[node]['hubscore']*SG.node[node]['hubscore']
 for node in SG.nodes():
     SG.node[node]['authscore']=float(SG.node[node]['authscore'])/math.sqrt(sumauth)
     SG.node[node]['hubscore']=float(SG.node[node]['hubscore'])/math.sqrt(sumhub)
 j+=1
dichub=dict()
dicauth=dict() 
#retrieving the hub score and authority score and sorting them
for node in SG.nodes():
    dichub[node]=SG.node[node]['hubscore']
    dicauth[node]=SG.node[node]['authscore']
d1 = collections.OrderedDict(sorted(dichub.items(), key=itemgetter(1),reverse=True))   
d2 = collections.OrderedDict(sorted(dicauth.items(), key=itemgetter(1),reverse=True))   
m=0
#priting the TOP 20 hubs and authorities with their higest score respectively
print "*******************Top 20 Hubs*******************"
for keys in d1:
 if d1[keys]!=0:
   m+=1
   if m<21:
      print "%s[%f] "%(keys,d1[keys])
print "********************Top 20 Authorities*******************"
m=0
for keys in d2:
 if d2[keys]!=0:
   m+=1
   if m<21:
      print "%s [%f]"%(keys,d2[keys]) 


