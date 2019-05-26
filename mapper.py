import json
import nltk
import re # remove digit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import itertools

def mapper(file, n, m): # n is the starting line, m is the ending line
	"""
	Read the json file, called preProcess()
	return: 4 mapper.txt files - with word tokenizer formatted as "word 1" line by line
	"""
	wd_lst = []
	json_dic = {}
	map_file_list = []
	# map_f = open(map_f, "w+")
	map_f = open("mapper"+str(n)+".txt", "w+")
	with open(file, 'r') as f:
	    try:
	        for line in itertools.islice(f, n, m):
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






