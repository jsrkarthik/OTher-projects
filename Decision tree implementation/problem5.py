import math
import networkx as nx
import pydot
import matplotlib.pyplot as plt
def main():
	list1=[1,'iRobot','Battery','ML-Based','Y']
	list2=[2,'iRobot','Gas','ML-Based','Y']
	list3=[3,'Honda','Gas','Alien tech','Y']
	list4=[4,'Boston Dynamics','Battery','Random planner','N']
	list5=[5,'Boston Dynamics','Gas','Alien tech','N']
	list6=[6,'iRobot','Battery','Alien tech','Y']
	list7=[7,'iRobot','Battery','Random planner','N']
	list8=[8,'iRobot','Gas','Alien tech','N']
	list9=[9,'Honda','Gas','AI algorithm','N']
	list10=[10,'Boston Dynamics','Battery','AI algorithm','N']
	list11=[11,'Boston Dynamics','Battery','ML-Based','Y']
	list12=[12,'Boston Dynamics','Gas','AI algorithm','Y']
	Manufacturer=['iRobot','Honda','Boston Dynamics']
	Power=['Battery','Gas']
	AI=['ML-Based','Alien tech','Random planner','AI algorithm']
	attributes=list()
	attributes.append(Manufacturer)
	attributes.append(Power)
	attributes.append(AI)
	data=list()
	data.append(list1)
	data.append(list2)
	data.append(list3)
	data.append(list4)
	data.append(list5)
	data.append(list6)
	data.append(list7)
	data.append(list8)
	data.append(list9)
	data.append(list10)
	data.append(list11)
	data.append(list12)
	"""i=0
	while i <12:
	  j=0
	  while j<5:
	    print data[i][j],
	    j+=1
	  i+=1
	  print "\n"  
	print Entropy(data)  
	"""
	#print "information gain=%f"%(informationgain(Manufacturer,data))
	G=pydot.Dot(graph_type='graph')
	#G=nx.DiGraph()
	root=builddecisiontree(G,data[:],attributes[:],0)
	G.write_png('example1_graph.png')
	#print G.nodes()
	#print G.edges()
	#nx.draw_circular(G)
	#plt.show()

    
def Entropy(data):
    nopex=0
    nonex=0
    i=0
    while i <len(data):
        if data[i][4]=='Y':
           nopex+=1
        elif data[i][4]=='N':
           nonex+=1
        i+=1
    #print nopex,nonex
    if nopex==0:
       poslog=0
    else:
       poslog=math.log(nopex*1.0/len(data),2)
    if nonex==0:
       nelog=0
    else:
       nelog=math.log(nonex*1.0/len(data),2)
    entropy=-((nopex*1.0/len(data))*poslog)-((nonex*1.0/len(data))*nelog)
    #print "returning entropy %f"%(entropy)
    return entropy
def printf(data):
    	print "printf called with lenofdata %d"%(len(data))
    	i=0
	while i <len(data):
	  j=0
	  while j<5:
	    print data[i][j],
	    j+=1
	  i+=1
	  print "\n"  

def informationgain(attrib,data):
     print "informationgain called with",
     print attrib,
     print data
     i=0
     sumvalattrib=0.0
     
     while i<len(attrib):
          modSV=0
          j=0
          templist=list()
          #print "lenofdata %d"%(len(data))
          while j<len(data):
             k=0
             while k<5:                
                if data[j][k]==attrib[i]:
                   templist.append(data[j])
                   #print data[j]
                   modSV+=1
                k+=1
             j+=1
          #printf(templist)   
          #print "modSV=%d"%(modSV)
          if len(templist)>0:
              sumvalattrib+=modSV*1.0/len(data)*Entropy(templist)    
          i+=1
     print "sumvalattrib=%f"%(sumvalattrib)
     gain=Entropy(data)-sumvalattrib     
     print "gain=%f"%(gain)
     return gain
    
def isallexamplesptve(data):
    i=0
    allptive=0    
    while i<len(data):
          if data[i][4]=='Y':
             allptive+=1             
          
          i+=1
    if allptive==len(data):
     return 1
    else: 
     return 0         

def isallexamplesntve(data):
    i=0
    allntive=0
    while i<len(data):
          if data[i][4]=='N':
             allntive+=1
          i+=1   
    if allntive==len(data):
       return 1
    else:
       return 0      

def newnode(node):
    print "creating new node",
    print node
    return [node,[],[],[]]
def createexamplevalues(value,data):
    i=0
    templist=list()
    while i<len(data):
     j=0 
     while j<5:
      if data[i][j]==value:
         templist.append(data[i])
      j+=1 
     i+=1 
    return templist   
    
def builddecisiontree(G,data,attributes,uniq): 

    uniq+=1
    print "builddecision tree called with",
    print data,
    root=''
    print attributes
    
    if len(data)==1 and len(attributes)==0:
       if data[0][4]=='Y':
          return 'Y.'+str(uniq)
       else:
          return 'N.'+str(uniq)
    elif len(data)==0 or len(attributes)==0:
       return ''
    if isallexamplesptve(data):
       root='Y.'+str(uniq)
       return root 
    elif isallexamplesntve(data):
       root='N.'+str(uniq)
       return root
    else:
       maxgain=0.0
       maxattr=' . '
       for attrib in attributes:
           gain=informationgain(attrib,data)
           if gain>maxgain:
               maxattr=attrib
               maxgain=gain
       print "Attribute chosen",
       print maxattr
       if 'iRobot' in maxattr:
          root='Manufacturer.'+str(uniq)
       elif 'Battery' in maxattr:
          root='Power.'+str(uniq)
       else:
          root='AI.'+str(uniq)   
       i=1
       for values in maxattr:
               uniq+=10
               templist=list()
               newdata=createexamplevalues(values,data)
  #             attributes.remove(maxattr)
               newattrib=list()
               for attr in attributes:
                   if attr!=maxattr:
                      newattrib.append(attr)
               print values
               lbl=root.split(".")
               if lbl[0]=='Y' or lbl[0]=='N':
                         fillcolo='red'
               else:
                         fillcolo='green'
               node1=pydot.Node(root,style='filled',fillcolor=fillcolo,label=lbl[0])
               if len(newdata)>0:	
                      tmp=builddecisiontree(G,newdata[:],newattrib[:],uniq)
                      lbl=tmp.split(".")
                      if lbl[0]=='Y' or lbl[0]=='N':
                         fillcolo='red'
                      else:
                         fillcolo='green'
                      node2=pydot.Node(tmp,style='filled',fillcolor=fillcolo,label=lbl[0])
                      G.add_node(node1)
                      G.add_node(node2)	
                      edge = pydot.Edge(node1,node2,value=values)
                      edge.set_label(values)
                      G.add_edge(edge)    
               #print G.edges   
               #root.insert(i,[builddecisiontree(newdata[:],newattrib[:]),[],[]])
               i+=1
    return root           
               
               
       
main()
