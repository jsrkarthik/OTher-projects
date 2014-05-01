import os
from os.path import basename
import re
srcdir="./ir"
dic=dict();
while True:
	inputstr=raw_input("Pls enter query")
	#inputstr="stanford University"
	mylist=inputstr.split()
	for path, dirs, files in os.walk(srcdir):
	     for filename in files:
		 fullpath = os.path.join(path,filename)
		 #print fullpath
		 if fullpath.endswith(".txt"):
		     f=open(fullpath,"r")
		     for line in f:
		         l=re.findall(r"[\w']+|[.,!?;]",line)
		         for i in l:
		             i=i.lower()
		             if not (i.find(".")!=-1 or i.find(",")!=-1 or i.find("?")!=-1 or i.find(";")!=-1):
		                 if i in dic:
		                     if not fullpath in dic[i]:
		                         dic[i].add(fullpath)                            
		                 else:
		                     dic[i]=set()
		                     dic[i].add(fullpath)
	result=set()
	if mylist[0].lower() in dic:
	    result=dic[mylist[0].lower()]
	for i in mylist:
	    i=i.lower()    
	    #print dic[i]
	    if i in dic:
		 result.intersection_update(dic[i])
	if not result:
	    print "No match found"
	else:
	    count=0
	    for i in result:
		 count+=1
		 print "%s"%(os.path.basename(i))
