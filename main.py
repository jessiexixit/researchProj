import sys
import os
import mapper
import reducer
import toK

def main():
	mapp = mapper(sys.argv[0])  # return a mapper.txt file
	# os.system("wc -l mapper.txt") ## ??????? 
	# I want to parse in the linux command, check how many lines in the mapper.txt file, and split into four files [map1.txt, map2.txt ... ]

	redu = reducer(mapp)  # reduce the mapper.txt
	mostCommon(redu, sys.argv[1])

	# multi threading to reduce files
	files_lst = ["map1.txt","map2.txt","map3.txt","map4.txt"]
	# reducer(files_lst)

	t1 = threading.Thread(target = reducer, args = ([files_lst[0]],))
	t2 = threading.Thread(target = reducer, args = ([files_lst[1]],))
	t3 = threading.Thread(target = reducer, args = ([files_lst[2]],))
	t4 = threading.Thread(target = reducer, args = ([files_lst[3]],))

	t1.start() 
	t2.start()
	t3.start()
	t4.start()

	t1.join()
	t2.join()
	t3.join()
	t4.join()


	reducer(["reducer.txt"])


if __name__ == "__main__":
   main()


