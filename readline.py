import json
import nltk
import numpy as np
import re # remove digit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

filename = "2014news1000.json"


def readfile(file):
	"""
	Read the json file into dictionary
	"""
	lst = []
	# count = 0
	with open(file, 'r') as f:
	    try:
	        while True:
	            line = f.readline()
	            if line:
	                r = json.loads(line)
	                lst.append(r)
	                # print(type(r))
	                # count+=1
	            else:
	                break
	       
	    except:
	    	# print(type(lst[0]["text"]))
	    	return lst
	    	f.close()


def extractText(lst):
	"""
	Extract the text into text list with punctuations
	"""
	text_list = []
	for i in range(len(lst)):
		text = lst[i]["text"].lower()
		text = re.sub(r'\d+', '', text)  # remove all numbers
		tokenizer = RegexpTokenizer(r'\w+')  ## remove all the punctuations

		a = tokenizer.tokenize(text)

		# a = nltk.word_tokenize(text)
		text_list += a
	# print(text_list)
	return text_list

def preProcess(lst):
	"""
	Remove all the punctuations and stop words 
	"""
	# english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
	# text_list = [word for word in lst if word not in english_punctuations]  # remove punctuations

	stops = set(stopwords.words("english")) 
	text_list = [word for word in lst if word not in stops]  # remove stope words
	porter = PorterStemmer()  # stem
	text_list = [porter.stem(word) for word in text_list]
	#print(text_list)
	return text_list

def mostCommon(lst,x):
	"""
	Find the xK most frequent words in the document
	"""
	freq_dist = nltk.FreqDist(lst)
	mst_freq = freq_dist.most_common(x*100)
	# mst_freq = mst_freq.keys()
	return mst_freq


# main
lst = [] 
n = int(input("Please enter the 10K most frequent you want to find: "))
json_lst = readfile(filename)
words_lst = extractText(json_lst)
words_lst_pre = preProcess(words_lst)
wd_count_lst = mostCommon(words_lst_pre,n)
for i in wd_count_lst:
	lst.append(i[0])
print(lst)



