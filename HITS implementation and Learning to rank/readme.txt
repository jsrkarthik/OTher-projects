                                           Home Work 2
Package contains hw2part1.py,hw2part2.py,output.pdf and homework2 files folder. Both files should be extracted to the same directory as homework2 files folder which has the input data 
Unzip the package hw2_322004061.tar.gz using tar command
tar -xzf hw2_322004061.tar.gz
hw2part1.py-
This file implements HITS algorithm on collection of tweets. 
hw2part2.py-
This file does the pair wise ranking algorithm and evaluation using SVM classifier
output.pdf contains the output of both part 1 and part 2 

To run the first program : 
1)use   command python hw2part1.py
2)output will be obtained in the console-for details check output.pdf
Remarks: I parsed the data using JSON libraries.I used DiGraph data structure from Networkx package to build and use graphs. For computation, i strictly followed HITS Algorithm and while updating hub scores and authority score, I updated both hub scores and authority scores based on the previous iternation but not the current iteration values which were giving different outputs.As prof mentioned, i followed this approach. i chose number of iterations as 622 as after that many iterations, values are converging to precision of 10^-5 difference.

To run the second program : 
1)use   command python hw2part2.py
2)output will be obtained in the console-for details  check output.pdf
Remarks: for second program, different penalties will give max accuracies for different folders(fold1,fold2,fold3). Details are mentioned in output.pdf. But the code has only  one value of c which may not give maximum value for all 3 folders at the same time. For evaluating the best accuracy for each folder, i experimented with different values of c and checked for the maximum output and reported that value in output.pdf .I used SVC with kernel = 'linear' argument but not the LinearSVC as professor mentioned anything is fine in the class

I took the help of piazza posts to complete the homework.
                            
