"""
topK.py file:
This file contain one function (mostCommon)
"""
import reducer

def mostCommon(file, x):
	"""
	Find the x thousand (1000x) most frequent words in the json document ("text")
	Store it in a list [[word,count], ... ], sorted the list
	Save only the top words in to a new list
	return: x thousand most frequent words list
	"""
	x = int(x)
	wd_lst = []
	line_lst = []
	lst = []
	with open(file, 'r') as f:
		for line in f:
			line_lst = line.strip().split()
			word = line_lst[0]
			count = int(line_lst[1])
			wd_lst.append([word, count])

	wd_lst.sort(key=lambda x: x[1], reverse = True) # sorted list reverse order 

	for i in range(x*1000):  # save top K word in new list
		lst.append(wd_lst[i][0])
		
	return lst

