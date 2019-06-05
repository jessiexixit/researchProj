from matrix import *
import sys

def main():
	file = sys.argv[1]
	wind_size = int(sys.argv[2])


	docTermMat, tf_mat = dtm(file, wind_size)
	termDocMat = tdm(docTermMat)
	idf_mat = idf(file, termDocMat, wind_size)
	tf_idf_mat = tf_idf(tf_mat, idf_mat)
	tar_rown = readWindowsz(file, wind_size)[1]
	print(similarTest(tf_idf_mat, tar_rown))

if __name__== "__main__":
	main()





