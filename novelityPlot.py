import numpy as np 
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages
from matrix import dateStore




def plot(simi_list, file):
	"""
	simi_list is a list of [row number of target news, row number of max similar news, similar number] first row has row number 1
	Plot a novelity graph with x = row number of target news, y = similar number
	"""
	x = []
	y = []
	dateTime_lst = dateStore(file)[1]

	for i in simi_list:
		# x.append(i[0])
		row_num = i[0]
		# print("test1---",row_num)
		x.append(dateTime_lst[row_num-1])
		# print("test2---",dateTime_lst[row_num])
		y.append(i[2])

	with PdfPages('picture/multipage_pdf'+str(x[0])+'.pdf') as pdf:  
		plt.title("2014 time vs Novelity") 
		plt.xlabel("time") 
		plt.ylabel("Novelity") 
		plt.plot(x,y)
		pdf.savefig()
		plt.close()

	# x axis label verticle