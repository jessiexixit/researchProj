"""
reduce.py: (mapreduce - reduce)
This file contains one function (reducer). 
Reading txt files generate by map. Create a reducer1.txt file with contain all the words and word counts from the json file - "text" part.
"""
import mapper

def reducer(files_lst):
	"""
	Read a list of 4 mapper.txt files, reduce the words into a reducer.txt file, and then reduce the reducer.txt file to reducer1.txt.
	return: reducer1.txt file.
	"""
	word_dic = {}
	
	if (files_lst[0] != "reducer.txt"):
		red_f = open("reducer.txt", "a+") # append the text, not overwritten
	if (files_lst[0] == "reducer.txt"):
		red_f = open("reducer1.txt", "w+")


	for i in range(len(files_lst)):
		file = files_lst[i]

		try:
			with open(file, 'r') as map_f:
				# print("what is files: ",files)
				for line in map_f:
					line_lst = line.strip().split()
					word = line_lst[0]
					count = int(line_lst[1])
					if word not in word_dic:
						word_dic[word] = count
					else:
						word_dic[word] += count
		except:
			file.close()

	# write the dictionary into reducer.txt file
	for i in word_dic:
		red_f.write("{} {}\n".format(i,word_dic[i]))

	return red_f


