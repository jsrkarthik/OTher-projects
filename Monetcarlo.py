import numpy as np
import random
n=1000
def pab(i,j,A,B):    
    num=0.0
    denom=0.0
    k=0
    while k<n:
      if A[k]==i and B[k]==j:
         num+=1
      if B[k]==j:
         denom+=1 
      k+=1
    return num*1.0/denom   


def pac(i,j,prob):
    num=0.0
    denom=0.0
    k=0
    while k<8:
      if prob[k][0]==i and prob[k][2]==j:
         num+=prob[k][3]
      if prob[k][2]==j:
         denom+=prob[k][3] 
      k+=1
    return num*1.0/denom   
         

def pbc(i,j,prob):
    num=0.0
    denom=0.0
    k=0
    while k<8:
      if prob[k][1]==i and prob[k][2]==j:
         num+=prob[k][3]
      if prob[k][2]==j:
         denom+=prob[k][3] 
      k+=1
    return num*1.0/denom   


def main():
	#pre-processing
	prob = np.array([[0,0,0,0.096], [0,0,1,0.048],[0,1,0,0.224],[0,1,1,0.012],[1,0,0,0.024],[1,0,1,0.432],[1,1,0,0.056],[1,1,1,0.108]], np.float64)
	"""i=0
	while i<8:
	  j=0
	  while j<4:
	    print prob[i][j],
	    j+=1
	  print "\n"
	  i+=1  """
	#pre-precossed ac,bc arrays
	probac=np.zeros((2,2))
	probbc=np.zeros((2,2))
	i=0
	while i<2:
	  j=0
	  while j<2:
	     probac[i][j]=pac(j,i,prob)
	     #print probac[i][j]
	     j+=1
	  i+=1   
	i=0
	while i<2:
	  j=0
	  while j<2:
	     probbc[i][j]=pbc(j,i,prob)
	     #print probbc[i][j]
	     j+=1
	  i+=1   
	#end of pre-processing  
	A=np.zeros((n))
	B=np.zeros((n))
	C=np.zeros((n))
	iteri=0
	while iteri<n:
	      #step1-calculate value of c
	      #randomly generate a value between 0 and 1
	      randc=random.random()
	      if randc>0.4:
	         C[iteri]=1
	      else:
	         C[iteri]=0
	      #step2- randomly generate a value between 0 and 1
	      #calculate value of B
	      randb=random.random()
	      if randb > probbc[C[iteri]][0]:
	         B[iteri]=1
	      else:
	         B[iteri]=0
	      #step3-Calculate value of A
	      #randomly generate a value between 0 and 1
	      randa=random.random()
	      if randa > probac[C[iteri]][0]:
	         A[iteri]=1
	      else:
	         A[iteri]=0
	      iteri+=1   
	"""i=0
	while i<n:
	  print "%d   %d   %d"%(A[i],B[i],C[i]) 
	  i+=1"""
	#  Step 5- Calculate value of AB matrix
	probab=np.zeros((2,2))
	i=0
	while i<2:
	  j=0
	  while j<2:
	     probab[i][j]=pab(j,i,A,B)
	     print probab[i][j],
	     j+=1
	  print "\n"   
	  i+=1   
  

main()	
