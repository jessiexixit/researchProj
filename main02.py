from matrix import *
from novelityPlot import *
from mapper import *
import os
import sys
from nltk import word_tokenize

def main():
	"""
	input: file, window_size, x_most_command word
	"""

	rules = """
    *-------------------* Instruction *-------------------------*
    *-----------------------------------------------------------*
    argument 1: file name / ex. 2014news1000.json
    argument 2: window size / ex. 15 for window size 15 days
	argument 3:	most command word in thousand / ex. 2 for 2000
	argument 4:	the company name you want to filtered / ex. IBM
	argument 5: Filter key in tile, main text or both 
				ex. 1 for title, 0 for main text, 2 for both
    """


	# print(rules)
	try:
		file = sys.argv[1]
		wind_size = int(sys.argv[2])
		maxx = int(sys.argv[3])
		key = sys.argv[4]
		flag = int(sys.argv[5])
	except IndexError:
		print(rules)


	# filter Company name
	# file = filterCompany(file, key, flag)
	# print("what is file: ",file)


	# length_file = sum(1 for line in file) 
	date_lst = dateStore(file)[0]  # all the unique date in the file in order
	# print("date_lst1: ", date_lst)

	while len(date_lst) <= 1:  # make sure at least two date in the list
		print("No such key word in file or no enought news to calculate")
		exit()


	date_lst = date_lst[0:(len(date_lst) - wind_size)] # the start date list
	while len(date_lst) == 0:
		wind_size = int(input("Please enter a smaller window size: "))
		date_lst = date_lst[0:(len(date_lst) - wind_size)] 



	# print("date_lst2: ",date_lst)

	cur_dir = os.getcwd()

	folder_name = 'picture'
	if os.path.isdir(cur_dir):
		if not os.path.exists('picture'):
			os.mkdir(os.path.join(cur_dir, folder_name))


	# read all the words token in the most frequent file and generate a mstCom_lst
	file_mstCom = "mostCommonWords"+str(maxx*1000)+".txt"

	if not os.path.isfile(file_mstCom): # if file_mstCom not exist, generate one 
		mstCom_lstToFile(mapreduce(file, maxx)) 

	with open(file_mstCom, 'r') as f: # now the file_mstCom definitly exist, read the file and get a most common words list
		mstCom_lst = []
		for line in f:
			mstCom_lst += word_tokenize(line)
	f.close()

	simi_list = []

	for i in date_lst:
		# mstCom_lst = mapreduce(file, maxx)
		docTermMat, tf_mat = documentTermMatrix(file, wind_size, i, mstCom_lst)  ##### date cannot just add 1
		termDocMat = termDocumentMatrix(docTermMat)
		idf_mat = IDF(file, termDocMat, wind_size, i)
		tf_idf_mat = TF_IDF(tf_mat, idf_mat)
		tar_rown = readWindowsz(file, wind_size, i)[1]
		date_count_dic = readWindowsz(file, wind_size, i)[2]
		simi_list += similarTest(tf_idf_mat, tar_rown, date_count_dic, i)



	print(simi_list)
	plot(simi_list, file, key, flag)
	print()





if __name__== "__main__":
	main()
