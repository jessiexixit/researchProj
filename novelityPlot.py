import numpy as np 
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages




def plot(simi_list):
	"""
	simi_list is a list of [row number of target news, row number of max similar news, similar number] first row has row number 1
	Plot a novelity graph with x = row number of target news, y = similar number
	"""
	x = []
	y = []

	for i in simi_list:
		x.append(i[0])
		y.append(i[2])

	with PdfPages('multipage_pdf'+str(x[0])+'.pdf') as pdf:  
		plt.title("2014 time vs Novelity") 
		plt.xlabel("time") 
		plt.ylabel("Novelity") 
		plt.plot(x,y)
		pdf.savefig()
		plt.close()

	#设置刻度，把x轴换成（年月日时间）