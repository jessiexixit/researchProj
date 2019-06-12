from matrix import *

import sys

def main():
	file = sys.argv[1]
	wind_size = int(sys.argv[2])
	maxx = int(sys.argv[3])

	# start_date = "20140101"

	# length_file = sum(1 for line in file) 
	date_lst = dateStore(file)
	# print("date_lst1: ", date_lst)
	date_lst = date_lst[0:(len(date_lst) - wind_size)]

	# print("date_lst2: ",date_lst)


	for i in date_lst:
		mstCom_lst = mapreduce(file, maxx)
		docTermMat, tf_mat = documentTermMatrix(file, wind_size, i, mstCom_lst)  ##### date cannot just add 1
		termDocMat = termDocumentMatrix(docTermMat)
		idf_mat = IDF(file, termDocMat, wind_size, i)
		tf_idf_mat = TF_IDF(tf_mat, idf_mat)
		tar_rown = readWindowsz(file, wind_size, i)[1]
		date_count_dic = readWindowsz(file, wind_size, i)[2]
		print(similarTest(tf_idf_mat, tar_rown, date_count_dic, i))
		print()


if __name__== "__main__":
	main()
