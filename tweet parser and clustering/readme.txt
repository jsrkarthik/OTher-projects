                                           Home Work 3
Package contains tweetcollector.py,cluster.py,graph.py and report.pdf
Unzip the package hw3_322004061.tar.gz using tar command
tar -xzf hw2_322004061.tar.gz
tweetcollector.py-
This file takes as input the query and returns the search results of tweet
cluster.py-
This file runs the tweet search over 32 queries given and creates 32 documents each containing 50 tweets with upto 1600 tweet collections.After this IT takes as input the value of K i.e number of clusters and gives the output creating k clusters with documents in them. Best values of RSS has been calculated by selecting random seeds for several iterations and displayed as well. Purity has been calculated for k=4 and displayed as well.

Graph.py contains the graph of K Vs RSS showing the relation between them.

report.pdf contains the detailed report containing the output for k=2,4,6,8 showing the RSS for each k.It contains the purity for k=4 and it also contains the graph of K Vs RSS



To run the tweetcollector.py
1)use   command python tweetcollector.py
2)Please enter the query
3) Results will be shown for each query
Remarks: I followed the instructions in the homework website.Experimented with different values of result_type and found recent value to be more appropriate

To run the cluster.py
1)use   command python cluster.py
2)Please enter the value of K/number of clusters
3) result clusters will be shown in the console
Remarks: I constructed document vector for each of 32 documents.I calculated the distance between document vectors using Cosine similarity as i found it to be more efficient and accurate than Euclidean distance. Followed the standard K-means algorithm, Calculated RSS with the help of Eculidean distance. Calculated  the purity as per standard definition

To run graph.py
1)use python graph.py
2)graph will be displayed
I took the help of piazza posts to complete the homework.
                            
