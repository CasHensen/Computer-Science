# Computer-Science
This repository contains the code that performs duplicate detection using Minhashing and LSH. Then using the candidate pairs from LSH a clustering method is applied to cluster the duplicates together. After this, the duplicate detection method is evaluated using the F1 score. 

The repository consists of a ReadMe file, the main.py, the functions.py and two extensions for 544966 and 535903. 

To implement the code the datafile TVs-all-merged.json needs to be downloaded from  https://canvas.eur.nl/courses/44014/files/90893251?module_item_id=1082427. 
The main.py script is the main entry point of the program and needs to be ran to obtain the results. The main.py implements the data cleaning, LSH and the clustering using the functions in the functions file. Furthermore, it outputs the evaluation metrics in different Excel files for each bootstrap. 
To implement the extensions the code in the functions file for the individual extensions needs to be uncommented in the clustering function. 
