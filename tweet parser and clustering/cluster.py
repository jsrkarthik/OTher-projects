#K-means clustering-@Author-JSR KARTHIK,Texas a&m
from os.path import basename
import tweepy
import time
import sys
from random import randint
import os   
import re  
import random
import math
import numpy as np
import copy


#function to calculate purity from groundtruth data.Purity is caluclated based on standard definition
def calcpurity(kcluster,groundtruth):
    i=0
    num=0.0
    while i<len(kcluster):
      a=np.zeros(4)
      for doc in kcluster[i]:
         if os.path.basename(doc) in groundtruth[0]:
            a[0]+=1
         elif os.path.basename(doc) in groundtruth[1]:
            a[1]+=1
         elif os.path.basename(doc) in groundtruth[2]:
            a[2]+=1
         elif os.path.basename(doc) in groundtruth[3]:
            a[3]+=1
      num+=maxval(a)         
      i+=1
    return num*1.0/32

#helper function to return the maximum value in an array-used mainly by calcpurity function
def maxval(a):
    i=0
    maxx=0
    while i<4:
       if a[i]>maxx:
         maxx=a[i]       
       i+=1    
    return maxx   
    

#Mean calculates the centroid of the cluster and returns it in the form of 1D numpy array. Just calculates the mean
def mean(clustlist,docvec,docmap):
    mean=np.zeros(len(docvec[0]))
    j=0
    while j<len(docvec[0]):
      i=0
      while i<len(clustlist):
        """print clustlist[i],
        print docmap[clustlist[i]],
        print docvec[docmap[clustlist[i]]]"""
        mean[j]+=docvec[docmap[clustlist[i]]][j]
        i+=1
      mean[j]=mean[j]/len(clustlist)
      j+=1
    #print mean   
    return mean

#A helper function that returns true if two centroid vectors are same
def issame(oldcentroid,newcentroid):
    i=0
    b=1
    while i<len(oldcentroid):
       j=0
       while j<len(oldcentroid[i]):
          if oldcentroid[i][j]!=newcentroid[i][j]:
             b=0
          j+=1
       i+=1      
    return b         


# Function that returns cosine distance between 2 vectors, Centroid and a document. Follows the standard defintion of cos distance
def cosinedist(docname,onedvec,twodvec):
    distnum=0.0
    j=0
    while j<len(onedvec):
        distnum+=twodvec[docname][j]*onedvec[j]
        j+=1
    j=0
    denom1=0.0
    while j<len(onedvec):
       denom1+=onedvec[j]*onedvec[j]
       j+=1
    j=0
    denom2=0.0
    while j<len(onedvec):
       denom2+=twodvec[docname][j]*twodvec[docname][j]
       j+=1   
    finaldist=distnum*1.0/(math.sqrt(denom1)*math.sqrt(denom2))
    return finaldist

#returns the euclidean distance between 2 vectors, used to calculate RSS
def euclideandist(docname,onedvec,twodvec):
    dist=0.0    
    j=0
    while j<len(onedvec):
        d=(twodvec[docname][j]-onedvec[j])
        dist+=d*d
        j+=1
    return math.sqrt(dist)
    
#recomputes centroud based on newly asigned clusters in K-means algorithm .Makes use of mean function to calculate mean of each element in the vector
def recomputecentroid(kcentroid,kcluster,docvec,k,docmap):
    i=0
    while i<k:
         kcentroid[i]=mean(kcluster[i],docvec,docmap)
         i+=1

def main():
	
	#data needed to obtain twitter data
	consumer_key = 'rcdbXbMyYAbaJ0DertwAjg'
	consumer_secret = 'JHcX2LVxxRZb9zgJi7J9j8my2Rvu6OHYbKM6HFjUKBI'
	access_key = '75150596-Y7hxPYCotMtrcBvXZ8sCsnGbLalgBBFJyS9PFDMR4'
	access_secret = 'Hi9LstuYQxR4sgfMfPyH4bqxnBkjVK2SSehyCnj2VKWmF'
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	i =0
	querylist=['#katyperry', '#katycats', '#darkhorse', '#iHeartRadio', '#ladygaga', '#TaylorSwift', '#sxsw', 'Rolling Stone','@DwightHoward', '#rockets', 'jeremy lin', 'toyota center', 'kevin mchale', 'houston nba', 'James Harden', 'linsanity','Jan Koum', 'WhatsApp', '#SEO', 'facebook', '#socialmedia', 'Zuckerberg', 'user privacy', '#Instagram','Obama', '#tcot', 'Russia', 'Putin', 'White House', 'Ukraine', 'Rand Paul', 'foreign policy']


	if not os.path.exists('./ir'):
             os.makedirs('./ir')
	#parsing through the list of queries to be clusterred and creating the document with tweet collection
	for query in querylist:
		i=0
		f=open('./ir/'+query+'.txt','w+')
		#api.search function searches through the twitter data and retrieves the results
		for tweet in api.search(q=query,count=50,		                  
				             result_type="recent",
				             include_entities=True,
				             lang="en"):
		    if i < 50 :
		     #print tweet.text
		     f.write(tweet.text.encode('utf-8'))
		     f.write('\n')
		     #print "\n"
		    else:
		     break
		    i+=1
		f.close()    
	while 1:	
		print "Pls enter number of clusters/K. Press 0 to quit"
		query=raw_input()
		k=int(query)
		if k==0:
		   break
		groundtruth=dict()
		# setting up the ground truth labels for calculating the purity
		groundtruth[0]=['#katyperry.txt', '#katycats.txt', '#darkhorse.txt', '#iHeartRadio.txt', '#ladygaga.txt', '#TaylorSwift.txt', '#sxsw.txt', 'Rolling Stone.txt']
		groundtruth[1]=['@DwightHoward.txt', '#rockets.txt', 'jeremy lin.txt', 'toyota center.txt', 'kevin mchale.txt', 'houston nba.txt', 'James Harden.txt', 'linsanity.txt']
		groundtruth[2]=['Jan Koum.txt', 'WhatsApp.txt', '#SEO.txt', 'facebook.txt', '#socialmedia.txt', 'Zuckerberg.txt', 'user privacy.txt', '#Instagram.txt']
		groundtruth[3]=['Obama.txt', '#tcot.txt', 'Russia.txt', 'Putin.txt', 'White House.txt', 'Ukraine.txt', 'Rand Paul.txt', 'foreign policy.txt']
		i =0
		#inverted index to store the documents and terms
		s=dict()
		filelist=list()
		srcdir="./ir"
		filelen=0
		#list of terms
		termlist=dict()
		visit=dict()
		count=0
		#traversing acroos the directory IR recusrsively where all the 32 documents with 1600 tweets are stored
		for path, dirs, files in os.walk(srcdir):
			     for filename in files:
				 fullpath = os.path.join(path,filename)
				 if fullpath.endswith(".txt"):
				     filelist.append(fullpath)
				     filelen+=1
				     f=open(fullpath,"r")
				     for line in f:
					  for i in re.split('[\W_]+', line) :#removing the punctuation
					      if len(i)==0:
						   continue
					      i=i.lower()
					      if i not in visit:
						   visit[i]=1
						   termlist[i]=count
						   count+=1
					     #calculating and populating the inverted index
					      if i in s: 
						       if fullpath in s[i]:                           
						          s[i][fullpath]+=1
						       else:                               
						          s[i][fullpath]=1
					      else:  
						          s[i]=dict();         
						          s[i][fullpath]=1


		i=0
		#storing the inverted index into document vector as 2D numpy array for faster access and calculations
		#map btw document name and document ID
		docmap=dict()
		for filename in filelist:
		    docmap[filename]=i
		    i+=1
		#Document vector
		docvec=np.zeros((32,len(termlist)))
		#map btw document number and document name
		dockey=dict()
		count=0
		for filen in filelist:
		    #docvec[docmap[filen]]=dict()
		    dockey[count]=filen
		    count+=1
		    #denom[filen]=0
		    f=open(filen,"r")
		    visit=dict()
		    for line in f:
			 #l=re.findall(r'\w+',line)
			 for i in re.split('[\W_]+', line):
			     if len(i)==0:
				  continue
			     i=i.lower()
			     if(i in visit):
				  continue
			     visit[i]=1
			     #calculating IDF of term		     
			     h=(filelen*1.0)/len(s[i])
			     #calculating TF*IDF of each term in document vector
			     x=(1+math.log10(s[i][filen]))*(math.log10(h))
			     #print " word N DF TF %s %d %d %d %s"%(i,filelen,len(s[i]),s[i][filen],filen)
			     #populating the document vector with TF*IDF weights
			     docvec[docmap[filen]][termlist[i]]=x
			     
		kcentroid=dict()	
		oldkcentroid=dict()
		i=0
		#K-means Algorithm starts here
		randlist=list()
		while i<k:
		    #randomly choosing initial seeds for K-means
		    
		    randdoc=random.randint(0, 31)
		    if randdoc not in randlist:
		       randlist.append(randdoc)
		    else:
		       continue   
		    kcentroid[i]=np.asarray(docvec[randdoc])
		  
		    i+=1
		oldkcentroid=copy.deepcopy(kcentroid)
		p=1
		didnotchange=0
		#dictionary holding the cluster of documents together
		kcluster=dict()
		#until the stopping criteria is met=>centroid and cclusters doesnt change over certain number of iterations
		while didnotchange<10:
			o=0		
			while o<k:
			    kcluster[o]=list()
			    o+=1
			i=0
			while i<32:
				 maxdist=0
				 nearestcentroid=0
				 j=0
				 while j<k:
				     #Caluclating the cosine similarity to find the nearest centroid. MAximim the cosine similarity, Near the document to the centroid
				     dist=cosinedist(i,kcentroid[j],docvec)
				     if dist>maxdist:
					 maxdist=dist
		 			 nearestcentroid=j
				     j+=1
				 kcluster[nearestcentroid].append(dockey[i])
				 i+=1 
	
			#  recomputing the centroids - by calculating the mean of the newly assigned clusters above
			recomputecentroid(kcentroid,kcluster,docvec,k,docmap)         
			#stopping criteria for the loop; When centroids stops changing, we stop the iterations
			if issame(oldkcentroid,kcentroid):
			   didnotchange+=1
			else:
			   didnotchange=0   
			#copy(oldkcentroid,kcentroid)
			#copying the current centroid to old centroid -used for stopping criteria of the algorithm		
			oldkcentroid=copy.deepcopy(kcentroid)
			p+=1    
		i=0
		#print "iteration %d"%(iteri)
		#priting the clusters finally
		while i<k:
		  print "cluster",
		  print i
		  print kcluster[i]
		  i+=1
		print "purity",
		#Calculating the purity as per standard definition
		print calcpurity(kcluster,groundtruth)
		i=0
		dist=0.0
		#calculating RSS-Residual sum of squares over all documents across all clusters which is used as measure to evaluate the quality of clustering
		while i<k:
		  for doc in kcluster[i]:
		     d=euclideandist(docmap[doc],kcentroid[i],docvec)
		     dist+=d*d
		  i+=1   
		print "RSS",
		print dist
		print "converged in %d iterations"%(p)     	
		
main()
