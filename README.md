# Computer-Science
This repository contains the code that performs duplicate detection using Minhashing and LSH. Then using the candidate pairs from LSH a clustering method is applied to cluster the duplicates together. After which the duplicate detection method is evaluated using the F1 score. 

The repository consists of a ReadMe file, the main.py, the functions.py and two extensions for 544966 and 535903. 
The main code implements the data cleaning, LSH and the clustering using the functions in the functions file. Furthermore, it outputs the evaluation metrics in different Excel files for each bootstrap. 
To implement the extensions the code in the functions file for the individual extensions needs to be uncommented in the clustering function. 
