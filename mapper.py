import json
import nltk
import numpy as np
import re # remove digit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import threading


def mapper(file):
	"""
	Read the json file, called def preProcess()
	return: mapper.txt file - with word tokenizer formatted as "word 1" line by line
	"""
	wd_lst = []
	map_f = open("mapper.txt", "w+")

	with open(file, 'r') as f:
	    try:
	        while True:
	            line = f.readline()

	            if line:
	                json_dic = json.loads(line) # generate dictionary one by one
	                wd_lst = preProcess(json_dic)
	                for i in wd_lst:    # write the after process word list into file mapper.txt
	                	map_f.write("{} {}\n".format(i,1))
	                # print("test 1")
	            else:
	            	break
	       
	    except:
	    	
	    	f.close()
	    	map_f.close()
	    	return map_f

def preProcess(json_dic):
	"""
	Extract the text into text list
	Remove all the punctuations and stop words 
	return: word tokenizer list after pre-processing
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



# main
# mapper("2014news1000.json")


