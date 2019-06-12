import json
from mapper import preProcess
from reducer import reducer
from topK import mostCommon
import numpy as np

from mapper import mapper
from reducer import reducer
from topK import mostCommon
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import multiprocessing


def readWindowsz(file, n, start_date):
	"""
	start_date is a string ("20140101")
	n: the window size we want to compare
	read a window size n and plus the target day, for example, 15 means (15+1 = 16 days). Parse the json into a dictionary and store all
	the dictionary in a list.
	return: 
	news_lst: list of news [{},{},{}...] 
	count_save: save the row number of the first news in the 16th day, which is the first target news (first row is 0)
	"""

	count = 0 # count line number
	current_date = "" # current date is the date of this current processing row 
	news_lst = [] 
	day = 0 # count how many day have already store in news_lst
	before_date = ""
	count_save = 0
	date_count_dic = {} # date is key, for each date how many row is value

	with open(file, 'r') as f:
		for line in f:
			json_dic = json.loads(line)
			count += 1
			before_date = current_date # store the last row date
			current_date = json_dic["dop"][:8]

			if (current_date not in date_count_dic):
				date_count_dic[current_date] = 1
			else:
				date_count_dic[current_date] += 1

			if (current_date >= start_date and current_date != before_date):
				day += 1
			if (int(current_date) - int(start_date) >= 0 and (day <= n + 1)): # If current date is equal or larger than start date and day count smaller than windown size + 1
				# if (current_date != )
				news_lst.append(json_dic)
				if (day < (n + 1)):  
						count_save += 1  

	f.close()



	return news_lst, count_save, date_count_dic

# print(readWindowsz("2014news1000.json", 1, "20140102")[2])

def dateStore(file):
	date_lst = []
	with open(file, 'r') as f:
		for line in f:
			json_dic = json.loads(line)
			date = json_dic["dop"][:8]
			if date not in date_lst:
				date_lst.append(date)



	return date_lst


def mapreduce(file, maxx):
	"""
	using map reduce, return the most command words list from the whole file
	return: the most command words list
	"""
	# count how many lines in file
	count = 0
	for line in open(file):
		count += 1

	line_split = int(count/4)

	# Read in the file once and build a list of line offsets
	line_offset = [0, line_split, 2*line_split, 3*line_split, count]  # [0, 1st break point, 2nd break point, 3rd break point]

	# multi threading to reduce files
	files_lst = ["mapper0.txt","mapper"+str(line_split)+".txt","mapper"+str(2*line_split)+".txt","mapper"+str(3*line_split)+".txt"]

	cpus = multiprocessing.cpu_count()

	with ThreadPoolExecutor(max_workers=cpus) as executor:
		for i in range(len(line_offset)-1):
			executor.submit(mapper, file, line_offset[i], line_offset[i+1])
			time.sleep(1)
			executor.submit(reducer, [files_lst[i]])
			time.sleep(1)


	reducer(["reducer.txt"])
	mstCom_lst = mostCommon("reducer1.txt", maxx)

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


def documentTermMatrix(file, n, start_date, mstCom_lst):
	"""
	n: how many days is a window size 
	call function readWindowsz, mapreduce, termFreqlist and generate a documentTermMatrix of a window size
	return: a numpy matrix
	"""
	lst = []
	tf_lst = []

	news_lst = readWindowsz(file, n, start_date)[0]
	# print("what is length of news_lst", len(news_lst))
	# mstCom_lst = mapreduce(news_lst)
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


def termDocumentMatrix(docTermMat):
	"""
	mtx: a document term matrix 
	return: term document matrix (a numpy matrix using transpose)
	"""
	termDocMat = np.transpose(docTermMat) # tdm is transpose of documentTermMatrix
	return termDocMat



def IDF(file, termDocMat, n, start_date):
	N = len(readWindowsz(file, n, start_date)[0])
	# print("N -------------------- ", N)
	count_t = np.count_nonzero(termDocMat, axis = 1)
	# print("what is count_t", count_t)
	idf = np.log(np.divide(N, (count_t + 1)))
	# print("idf --------------- ", idf)
	return idf


def TF_IDF(tf_mat, idf):
	idf = np.transpose(idf)
	return np.multiply(tf_mat, idf)



def similarTest(tf_idf_mat, tar_rown, date_count_dic, start_date):
	"""
	tf_idf_mat: the tf_idf of 1-16 days
	tar_rown: the row number of the 1 news of 16 days
	"""
	max_simi = 0
	simi_list = [] # [row number of target news, row number of max similar news, similar number] first row has row number 1
	row_summ = 0 

	new_news_mat = tf_idf_mat[tar_rown:,]
	old_news_mat = tf_idf_mat[:tar_rown,]

	# print("tar_rown",tar_rown)
	# print("lenght of tf_idf_mat", len(tf_idf_mat))
	# print("new_news_mat",len(new_news_mat))
	# print("old_news_mat",len(old_news_mat))

	for i in date_count_dic:
		if (int(i) <  int(start_date)):
			row_summ += date_count_dic[i]


	for i in range(len(new_news_mat)):
		item = new_news_mat[i,]
		item = np.transpose(item)
		# print("item", item)
		simi = old_news_mat.dot(item)
		# print("simi", simi)
		max_value = np.max(simi)
		# print("max_value", max_value)
		# print("what is max_value ========= ", max_value)
		max_index = np.argmax(simi)
		# print("what is max_index ========== ", max_index)
		simi_list.append([i + len(old_news_mat) + row_summ + 1, max_index + row_summ + 1, max_value])
	# print("what is simi_lst", simi_list)
	return simi_list






