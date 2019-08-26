# News Novelity 
Project Description:
This natural language project is aimed to determine whether the database news is new published by calculate the TF-IDF and plot the novelity plot filtered by company name.

Files contain:
•	main02.py
running operation:
input the following argument one by one

argument 1: file name / ex. 2014news1000.json
    	argument 2: window size / ex. 15 for window size 15 days
	argument 3:	most command word in thousand / ex. 2 for 2000
	argument 4:	the company name you want to filtered / ex. IBM
	argument 5: Filter key in tile, main text or both 
				ex. 1 for title, 0 for main text, 2 for both

•	clean_json.py
Fixing the single and double quotation reading problem in json format. Outputting the program readable json file.

•	matrix.py
Read the window size data and using map reduce to generate the most command words list. Calculating the DTM, TDM, TF-IDF and save the maximum negative logarithm TF-IDF as the novelity number which followed by the similar row number. 

•	mapper.py
This file contains two function (mapper, preProcess). 
Using the json file as system input, read json file line by line and generate dictionary line by line.
json file line format: {"url": " ", "title": " ", "dop": " ", "text": " "}
Extract the words in "text", doing preprocessing and generate a words token list. Store the words in the mapper.txt file.

•	topK.py
Find the x thousand (1000x) most frequent words in the json document ("text")
Store it in a list [(count, word), ... ], sorted the list
	Save only the top words in to a new list
	return: x thousand most frequent words list

•	reducer.py
reduce.py: (mapreduce - reduce)
This file contains one function (reducer). 
Reading txt files generate by map. Create a reducer1.txt file with contain all the words and word counts from the json file - "text" part.

