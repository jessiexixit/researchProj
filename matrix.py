import json
from mapper import preProcess
from reducer import reducer
from topK import mostCommon
import numpy as np


def readWindowsz(n):
	"""
	read a window size n, for example 15 means (15 days)
	return: list of news [{},{},{}...]
	"""

	count = 0 # count number of line
	pre_count = 0 
	date = ""
	day = 0 # count number of day
	# days_offset_lst = [0]
	news_lst = []

	# f = open("2014news1000.json")

	with open("2014news1000.json", 'r') as f:
		try:
			for line in f:
				if line:
					json_dic = json.loads(line)
					news_lst.append(json_dic)
					count += 1
					# print("what is date: ",json_dic["dop"][:8]) 
					if (json_dic["dop"][:8] != date):
						day += 1
						date = json_dic["dop"][:8]
		except:
			f.close()

	# print("what is count: ", count)
	# print("what is pre_count: ", pre_count)
	# print("what is date: ", date)
	# print("what is day: ", day)
	return news_lst




def mapreduce(news_lst):
	"""
	for all of the words in the window set, find the most thousand common word
	return: the most command words list
	"""
	map_f = open("tf.txt", "w")
	# print("!!!")
	for json_dic in news_lst:

		wd_lst = preProcess(json_dic)
		for i in wd_lst:    # write the after process word list into file mapper.txt
			map_f.write("{} {}\n".format(i,1))
			# print("!!!")

	map_f.close()
	reducer(["tf.txt"])
	reducer(["reducer.txt"])
	mstCom_lst = mostCommon("reducer1.txt", 1)  ####### make change here !!!!!!!!!!!!!!!!!!!
	return mstCom_lst



def newsTotokenDic(news):
	"""
	For each news, generate a word_dic with word as key and word count as value
	return: word_dic (a dictionary)
	"""
	word_dic = {}
	token_lst = preProcess(news)
	for word in token_lst:
		if (word not in word_dic):
			word_dic[word] = 1
		else:
			word_dic[word] += 1


	return word_dic


def termFreqlist(mstCom_lst, news):
	"""
	check for each words in the most comment list, how many of them are in the news article.
	news: each json article
	return: a term frequency for a document
	"""
	lst_of_lst = [0] * len(mstCom_lst)
	count = 0


	topK_dic = {}
	index_lst = [n for n in range(len(mstCom_lst))]
	topK_dic = dict(zip(mstCom_lst, index_lst)) # store most frequent word and index 

	word_dic = newsTotokenDic(news)

	for i in topK_dic:
		if i in word_dic:
			count = word_dic[i]
			lst_of_lst[topK_dic[i]] = count

	return lst_of_lst


def dtm(n):
	lst = []
	# lst.append(lst_of_lst)
	news_lst = readWindowsz(n)
	# print("what is length of news_lst", len(news_lst))
	mstCom_lst = mapreduce(news_lst)
	# print("what is length of mstCom_lst", len(mstCom_lst))

	for i in range(len(news_lst)):
		# wd_dic = newsTotokenDic(news_lst[i])
		lst_of_lst = termFreqlist(mstCom_lst,news_lst[i])
		lst.append(lst_of_lst)
	# use numpy to create a matrix
	# print("what is length of lst", len(lst))
	mtx = np.matrix(lst)

	return mtx



# main
# news_lst = readWindowsz(1) # read all of the first day json and store in news_lst
# mstCom_lst = mapreduce(news_lst) # find the most common word list in first day
# # for news in news_lst:
# print(newsTotokenDic(news_lst[0])) # count the first news
# list_of_lst = termFreqlist(mstCom_lst,news_lst[0])
# # write a for loop to store every term freq list into dtm


print(dtm(1))







