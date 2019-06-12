"""
mapper.py file: (mapreduce - map)
This file contains two function (mapper, preProcess). 
Using the json file as system input, read json file line by line and generate dictionary line by line.
json file line format: {"url": " ", "title": " ", "dop": " ", "text": " "}
Extract the words in "text", doing preprocessing and generate a words token list. Store the words in the mapper.txt file.
"""

import json
import nltk
import re # remove digit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import itertools

def mapper(file, n, m): # n is the starting line, m is the ending line. (first line is 0)
	"""
	Read the json file line by line and called preProcess() function 
	return: four mapper.txt files. The mapper.txt files contain word tokenizer formatted as "word" 1 line by line. 
	"word" is the actual word, 1 is the count.
	"""
	wd_lst = []
	json_dic = {}
	map_file_list = []
	# map_f = open(map_f, "w+")
	map_f = open("mapper"+str(n)+".txt", "w+")
	with open(file, 'r') as f:
		for line in itertools.islice(f, n, m): # read the file start from row n to row m
			json_dic = json.loads(line) # load json to generate dictionary 
			wd_lst = preProcess(json_dic)
			for i in wd_lst:    # write the processed word list into mapper.txt file
				map_f.write("{} {}\n".format(i,1))
		        # print("test 1")

	    	
	f.close()
	map_f.close()
	return map_f

# def multi_run_wrapper(args):
# 	return mapper(*args)

def preProcess(json_dic):
	"""
	json_dic: This is the dictionary after reading the json file, one line is one dictionary
	Extract the "text" in the dictionary into token list
	Remove all the punctuations, transform to lower case, remove stop words, number, special charaters, stemming
	return: word tokenizer list after pre-processing (word_lst)
	"""
	word_lst = []
	text = json_dic["text"].lower() # words string
	# text = word_lst[i]["text"].lower()
	text = re.sub(r'\d+', '', text)  # remove all numbers
	# text = ''.join(c for c in text if not c.isdigit())
	tokenizer = RegexpTokenizer(r'\w+')  # remove all punctuations

	word_lst = tokenizer.tokenize(text)

	stops = set(stopwords.words("english"))  # set stop words list
	word_lst = [word for word in word_lst if word not in stops]  # remove stope words  
	word_lst = [word for word in word_lst if word.isalpha()] # remove words with special characters
	porter = PorterStemmer()  # stemming 
	word_lst = [porter.stem(word) for word in word_lst]

	return word_lst






