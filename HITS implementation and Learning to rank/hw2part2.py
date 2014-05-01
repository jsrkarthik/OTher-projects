import re
from scipy.sparse import lil_matrix
import numpy as np
from sklearn import svm
import collections
from operator import itemgetter
import os
# pre processing a file and forming a dictionary containing queries feautures
def preprocess(filename):
	fullpath=filename
	f=open(fullpath,"r")
	dic=dict()
	count=1
	for line in f:
	   lis=line.split()  	   
	   idd=lis[1].split(':')
	   if idd[1] in dic: 
		if lis[0] in dic[idd[1]]:
		   dic[idd[1]][lis[0]][count]=list()		   
		   k=2
		   while k < len(line.split()):
		       dic[idd[1]][lis[0]][count].append((lis[k].split(':')[1]))
		       k+=1
		else:
		   dic[idd[1]][lis[0]]=dict()         
		   dic[idd[1]][lis[0]][count]=list()
		   k=2
		   while k < len(line.split()):
		        dic[idd[1]][lis[0]][count].append((lis[k].split(':')[1]))
		        k+=1		
	   else:
		count=1
		dic[idd[1]]=dict()
		dic[idd[1]][lis[0]]=dict()
		dic[idd[1]][lis[0]][count]=list()
		k=2
		while k < len(line.split()):
		       dic[idd[1]][lis[0]][count].append(lis[k].split(':')[1])
		       k+=1		
	   count+=1
	return dic  
# this function builds pairs and input array for SVM-Input array-array of nsamples,40 feautures
def buildpairsandinparray(dic,array,lenn):   
   label = np.zeros((lenn,))  
   c=0	
   for query in dic:     
     dicpair=dict()
     for rel in dic[query]:
         for rel1 in dic[query]:
             if rel!=rel1:
                for k1 in dic[query][rel]:
                    for k2 in dic[query][rel1]:
                      dicpair[c]=list()
                      dicpair[c].append(k1)
                      dicpair[c].append(k2)                      
                      if int(rel)-int(rel1) > 0:
                         label[c] = 1
                      else:                        
                         label[c] = -1
                      p=0                      
                      while  p < 40:                          
                          array[c][p] = float(dic[query][rel][k1][p])-float(dic[query][rel1][k2][p])                         
                          p+=1
                      c+=1                      
   return label
#function to return the number of elements in the dictionary-used to intialize numpy arrays
def countnumberofpairs(dic):
    c=0
    for query in dic:     
      for rel in dic[query]:
         for rel1 in dic[query]:
             if rel!=rel1:
                for k1 in dic[query][rel]:
                    for k2 in dic[query][rel1]:
                        c+=1
    
    return c    
    
def main():
 srcdir='./homework2 files'

 for path, dirs, files in os.walk(srcdir):
  if 'fold' in path:   
    penalty=1.0
    #penalty value is chosen according to folder ,
    # For folder1 0.4,folder2 8.3, folder3 0.1 gave the maximum accuracy(found it by experimentation with penalty values-between 0-50
    dic=dict()
    #first processing the train data and fit into SVM classifier
    dic=preprocess(path+'/train.txt')    
    lenn=0
    lenn=countnumberofpairs(dic)
    array = np.zeros(shape=(lenn, 40))        
    label=buildpairsandinparray(dic,array,lenn)
    #using the SVC of the SVM classifier to classify- Traning the SVC with train data
    clf = svm.SVC(kernel="linear",C=penalty)    
    clf.fit(array, label) #train data fitting is done. 
    dicfeauture=dict()
    k=0
    #processing the Coefficient vector and storing it in dictionary
    temp=clf.coef_
    while k<40:  
          dicfeauture[k]=list()
          dicfeauture[k].append(abs(temp[0][k]))
          if temp[0][k]<0:
             dicfeauture[k].append(-1)
          else:
             dicfeauture[k].append(1)
          k+=1
    
    #now test data, First obtain the test data values from pairwise algorithm and retrieve the output in label array
    dic=preprocess(path+'/test.txt')    
    lenn=countnumberofpairs(dic)
    array = np.zeros(shape=(lenn, 40))   

    label=buildpairsandinparray(dic,array,lenn)
    # Evaluating -> retrieving the output from classfier prediction and comparing it with the output of the classifier algoirthm to see how many are correct?
    labl=clf.predict(array)
    r=0
    correct =0    
    while r < lenn:
       if labl[r] == label[r]:
          correct+=1
       r+=1        
    print "accuracy for %s =%f"%((os.path.basename(path)),float(correct*100)/lenn)
    d1 = collections.OrderedDict(sorted(dicfeauture.items(), key=itemgetter(1),reverse=True))  
    print "coef_ Top 10 Feauture Vectors"
    m=0
    #priting the right feature number-as some are missing
    for keyy in d1:
         if m<10:   
           if d1[keyy][1]<0:
              d1[keyy][0]=d1[keyy][0]*-1
           if keyy<=4:
              keyprint = keyy+1
           elif keyy<=36:
              keyprint = keyy+6
           elif keyy<=39:
              keyprint = keyy+7
           print "feauture-%d   %f"%(keyprint,d1[keyy][0])
         m+=1    

main()
