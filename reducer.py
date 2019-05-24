import mapper
import threading

def reducer(files):
	word_dic = {}
	token_lst = []
	
	# reduce the reducer.txt, need overwritten
	if (files != "reducer.txt"):
		red_f = open("reducer.txt", "a+") # append the text, not overwritten
	else:
		red_f = open("reducer1.txt", "w+")
	# print("!!!!!",files)

	with open(files, 'r') as map_f:
		# print("what is files: ",files)

		data = []
		for line in map_f:
			line_lst = line.strip().split()
			word = line_lst[0]
			count = int(line_lst[1])
			if word not in word_dic:
				word_dic[word] = count
			else:
				word_dic[word] += count

	# write the dictionary into reducer.txt file
	
	for i in word_dic:
		# print("what is type",type(i))
		red_f.write("{} {}\n".format(i,word_dic[i]))

	return red_f


# main
# files_lst = ["map1.txt","map2.txt","map3.txt","map4.txt"]

# t1 = threading.Thread(target = reducer, args = (files_lst[0],))
# t2 = threading.Thread(target = reducer, args = (files_lst[1],))
# t3 = threading.Thread(target = reducer, args = (files_lst[2],))
# t4 = threading.Thread(target = reducer, args = (files_lst[3],))

# t1.start() 
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()


# reducer("reducer.txt")


