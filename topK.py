
import reducer

def mostCommon(file, x):
	"""
	Find the xK most frequent words in the document
	"""
	# freq_dist = nltk.FreqDist(lst)
	# mst_freq = freq_dist.most_common(x*100)
	# # mst_freq = mst_freq.keys()
	# return mst_freq

	wd_lst = []
	line_lst = []
	lst = []
	with open(file, 'r') as f:
		for line in f:
			line_lst = line.strip().split()
			word = line_lst[0]
			count = int(line_lst[1])
			wd_lst.append([word, count])

	wd_lst.sort(key=lambda x: x[1], reverse = True) # sorted list reverse order 

	for i in range(x*1000):  # save top K word in new list
		lst.append(wd_lst[i][0])
		
	return lst



