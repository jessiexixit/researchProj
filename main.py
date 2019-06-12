import sys
from mapper import mapper
from reducer import reducer
from topK import mostCommon
from concurrent.futures import ThreadPoolExecutor
import time
import threading


from multiprocessing import Pool
import multiprocessing


def main():
	file = sys.argv[1]
	count = 0 # line count

	# count how many lines in file
	# count = sum(1 for line in open(file))
	count = 0
	for line in open("2014news1000.json"):
		count += 1

	line_split = int(count/4)

	# Read in the file once and build a list of line offsets
	line_offset = [0, line_split, 2*line_split, 3*line_split, count]  # [0, 1st break point, 2nd break point, 3rd break point]

	# multi threading to reduce files
	files_lst = ["mapper0.txt","mapper"+str(line_split)+".txt","mapper"+str(2*line_split)+".txt","mapper"+str(3*line_split)+".txt"]


	with ThreadPoolExecutor(max_workers=4) as executor:
		for i in range(len(line_offset)-1):
			executor.submit(mapper, file, line_offset[i], line_offset[i+1])
			time.sleep(1)
			executor.submit(reducer, [files_lst[i]])
			time.sleep(1)


	reducer(["reducer.txt"])
	print(mostCommon("reducer1.txt", sys.argv[2]))


if __name__== "__main__":
	main()





