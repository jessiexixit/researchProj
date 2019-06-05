import json
from mapper import preProcess
from reducer import reducer
from topK import mostCommon
import numpy as np


def readWindowsz(file, n):
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

	with open(file, 'r') as f:
		for line in f:
			if (day <= (n + 1)):
				json_dic = json.loads(line)
				news_lst.append(json_dic)
				count += 1
				if (json_dic["dop"][:8] != date):
					day += 1
					date = json_dic["dop"][:8]
					if (day == (n + 1)):
						count_save = count - 1  # save the row number of 16th day, first row is 0

	f.close()

	return news_lst, count_save




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
	mstCom_lst = mostCommon("reducer1.txt", 2)  ####### make change here !!!!!!!!!!!!!!!!!!!
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

	return lst_of_lst, word_dic


def dtm(file, n):
	"""
	n: how many days is a window size 
	call function readWindowsz, mapreduce, termFreqlist and generate a dtm of a window size
	return: a numpy matrix
	"""
	lst = []
	tf_lst = []

	news_lst = readWindowsz(file, n)[0]
	# print("what is length of news_lst", len(news_lst))
	mstCom_lst = mapreduce(news_lst)
	# print("what is length of mstCom_lst", len(mstCom_lst))

	for i in range(len(news_lst)):
		# wd_dic = newsTotokenDic(news_lst[i])
		lst_of_lst = termFreqlist(mstCom_lst,news_lst[i])[0]
		word_dic = termFreqlist(mstCom_lst,news_lst[i])[1]
		lst.append(lst_of_lst)
		lst_of_lst = np.array(lst_of_lst)
		tf = np.divide(lst_of_lst, sum(word_dic.values()))
		# print(sum(word_dic.values()))
		tf = tf_lst.append(tf)
		
	# use numpy to create a matrix
	# print("what is length of lst", len(lst))
	docTermMat = np.matrix(lst)
	tf_mat = np.matrix(tf_lst)

	return docTermMat, tf_mat


def tdm(docTermMat):
	"""
	mtx: a document term matrix 
	return: term document matrix (a numpy matrix using transpose)
	"""
	termDocMat = np.transpose(docTermMat) # tdm is transpose of dtm
	return termDocMat



def idf(file, termDocMat, n):
	N = len(readWindowsz(file, n)[0])
	# print("N -------------------- ", N)
	count_t = np.count_nonzero(termDocMat, axis = 1)
	# print("what is count_t", count_t)
	idf = np.log(np.divide(N, (count_t + 1)))
	# print("idf --------------- ", idf)
	return idf


def tf_idf(tf_mat, idf):
	idf = np.transpose(idf)
	return np.multiply(tf_mat, idf)


def similarTest(tf_idf_mat, tar_rown):
	"""
	tf_idf_mat: the tf_idf of 1-16 days
	tar_rown: the row number of the 1 news of 16 days
	"""
	max_simi = 0
	simi_list = [] # [row number of target news, row number of max similar news, similar number] (1st row is index 0)

	new_news_mat = tf_idf_mat[tar_rown:,]
	old_news_mat = tf_idf_mat[:tar_rown,]

	for i in range(len(new_news_mat)):
		item = new_news_mat[i,]
		item = np.transpose(item)
		simi = old_news_mat.dot(item)
		max_value = np.max(simi)
		# print("what is max_value ========= ", max_value)
		max_index = np.argmax(simi)
		# print("what is max_index ========== ", max_index)
		simi_list.append([i + len(old_news_mat), max_index, max_value])
	# print("what is simi_lst", simi_list)
	return simi_list






