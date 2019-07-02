import numpy as np 
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
from matrix import dateStore




def plot(simi_list, file, key, flag):
	"""
	simi_list is a list of [row number of target news, row number of max similar news, similar number] first row has row number 1
	Plot a novelity graph with x = row number of target news, y = similar number
	"""

	if int(flag) == 1:
		title = "2014 "+key+" in title"
	elif int(flag) == 0:
		title = "2014 "+key+" in text"
	elif int(flag) == 0:
		title = "2014 "+key+" in both title & text"



	x = []
	y = []
	dateTime_lst = dateStore(file)[1]
	# dateTime_lst = dateStore(file)[0]

	for i in simi_list:
		# x.append(i[0])
		row_num = i[0]
		# print("test1---",row_num)
		x.append(dateTime_lst[row_num-1])
		# print("test2---",dateTime_lst[row_num])
		y.append(i[2])


	with PdfPages('picture/'+title+'.pdf') as pdf:  
		plt.title(title) 
		plt.xlabel("time", fontsize = 10) 
		plt.ylabel("Novelity") 
		plt.xticks(rotation=90, fontsize=4)

		plt.plot(x,y)
		pdf.savefig()
		plt.close()

	# x axis label verticle