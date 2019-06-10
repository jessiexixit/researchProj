from matrix import *
import sys

def main():
	file = sys.argv[1]
	wind_size = int(sys.argv[2])

	start_date = "20140101"

	# length_file = sum(1 for line in file) 
	date_lst = dateStore(file)
	# print("date_lst1: ", date_lst)
	date_lst = date_lst[0:(len(date_lst) - wind_size)]

	# print("date_lst2: ",date_lst)

	# read and add the 17days
	# for i in range(length_file - wind_size):
		# readWindowsz(file, n, str(int(start_date) + i))

	for i in date_lst:
	# i = "20140101"

		docTermMat, tf_mat = documentTermMatrix(file, wind_size, i)  ##### date cannot just add 1
		termDocMat = termDocumentMatrix(docTermMat)
		idf_mat = IDF(file, termDocMat, wind_size, i)
		tf_idf_mat = TF_IDF(tf_mat, idf_mat)
		tar_rown = readWindowsz(file, wind_size, i)[1]
		print(similarTest(tf_idf_mat, tar_rown))

if __name__== "__main__":
	main()

