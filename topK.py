"""
topK.py file:
This file contain one function (mostCommon)
"""
import reducer
from queue import Queue
from queue import PriorityQueue
from nltk.tokenize import RegexpTokenizer


class ReversePriorityQueue(PriorityQueue):
	def put(self, tup):
	    newtup = tup[0] * -1, tup[1]
	    PriorityQueue.put(self, newtup)

	def get(self):
	    tup = PriorityQueue.get(self)
	    newtup = tup[0] * -1, tup[1]
	    return newtup



def mostCommon(file, x):
	"""
	Find the x thousand (1000x) most frequent words in the json document ("text")
	Store it in a list [(count, word), ... ], sorted the list
	Save only the top words in to a new list
	return: x thousand most frequent words list
	"""
	x = int(x)
	q = ReversePriorityQueue() ###
	lst = []

	with open(file, 'r') as f:
		for line in f:
			tokenizer = RegexpTokenizer(r'\w+')  # remove all punctuations
			line_lst = tokenizer.tokenize(line)
			# print(line_lst)
			word = line_lst[0]
			# print(word)
			count = int(line_lst[1])
			# print(count)
			q.put((count, word))


	 
	for i in range(x*1000):  # save top K word in new list
		lst.append(q.get()[1])
	
	return lst

# lst = mostCommon("test_topk.txt",1)
# print(lst)



