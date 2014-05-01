import os
from os.path import basename
import re 
import collections
import math
from operator import itemgetter
s=dict()
filelist=list()
srcdir="./ir"
filelen=0
while True:
	inputstr=raw_input("Pls enter query")
	#inputstr="information storage and retrieval"
	mylist=inputstr.split()
	for path, dirs, files in os.walk(srcdir):
	     for filename in files:
		 fullpath = os.path.join(path,filename)
		 #print fullpath
		 if fullpath.endswith(".txt"):
		     filelist.append(fullpath)
		     filelen+=1
		     f=open(fullpath,"r")
		     for line in f:
		         #l=re.findall(r'\w+',line)
		         for i in re.split('[\W_]+', line) :
		             if len(i)==0:
		                 continue
		             i=i.lower()
		             #if not (i.find(".")!=-1 or i.find(",")!=-1 or i.find("?")!=-1 or i.find(";")!=-1):
		             if i in s: 
		                     if fullpath in s[i]:                           
		                        s[i][fullpath]+=1
		                     else:                               
		                        s[i][fullpath]=1
		             else:  
		                        s[i]=dict();         
		                        s[i][fullpath]=1

	#for keys in s:
	   #for keeys in s[keys]:
		#print "%s%s%d"%(keys,keeys,s[keys][keeys])                       
	k=0
	query=dict()
	cosdic=dict()

	denom=dict()
	for filen in filelist:
	    denom[filen]=0
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
		     #if not (i.find(".")!=-1 or i.find(",")!=-1 or i.find("?")!=-1 or i.find(";")!=-1):
		     h=(filelen*1.0)/len(s[i])
		     x=(1+math.log10(s[i][filen]))*(math.log10(h))
		     #print " word N DF TF %s %d %d %d %s"%(i,filelen,len(s[i]),s[i][filen],filen)
		     denom[filen]+=x*x
		         
		         
	for i in mylist:
	    i=i.lower()
	    if i not in query:
		 query[i]=1
	    else:
		 query[i]+=1
	temp=0
	for i in query:
	    temp+=query[i]*query[i]

	for filen in filelist:        
	    cosdic[filen]=0
	    for keys in query:
		    if keys in s:
		            f=open(filen,"r")
		            found=0
		            for line in f:
		                #l=re.findall(r'\w+',line)
		                for i in re.split('[\W_]+', line) :
		                    if len(i)==0:
		                        continue                          
		                    i=i.lower()
		                    if i==keys:
		                        found=1
		                        break
		            if found==1:
		                #print "%s %s\n"%(keys,filen)
		                #print " %s %f %f %f\n"%(keys,math.log10(query[keys]),math.log10((s[keys][filen])),math.log10(filelen/(len(s[keys]))))
		                cosdic[filen]+=(query[keys])*(1+math.log10((s[keys][filen])))*(math.log10(filelen/(len(s[keys]))))
	    cosdic[filen]=(cosdic[filen])*(1/math.sqrt(temp))*(1/math.sqrt(denom[filen]))

	d = collections.OrderedDict(sorted(cosdic.items(), key=itemgetter(1),reverse=True))   
	m=0
	for keys in d:
	 if d[keys]!=0:
	   m+=1
	   if m<51:
		print "%s [ %f ] "%(os.path.basename(keys),d[keys])
	if m==0:
	 print "Sorry no match found for your query"
