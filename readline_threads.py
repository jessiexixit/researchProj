import json
# import nltk
# import numpy as np
# from nltk.tokenize import RegexpTokenizer
# from nltk.corpus import stopwords

# filename = "2014news1000.json"


def readfile(file):
	"""
	Read the json file into dictionary
	"""
	lst = []
	# count = 0
	with open(file, 'r') as f:
	    try:
	        while True:
	            line = f.readline()
	            if line:
	                r = json.loads(line)
	                lst.append(r)
	                # print(type(r))
	                # count+=1
	            else:
	                break
	       
	    except:
	    	# print(type(lst[0]["text"]))
	    	return lst
	    	f.close()


def extractText(lst):
	"""
	Extract the text into text list with punctuations
	"""
	text_list = []
	for i in range(len(lst)):
		text = lst[i]["text"].lower()

		tokenizer = RegexpTokenizer(r'\w+')  ## remove all the punctuations
		a = tokenizer.tokenize(text)

		# a = nltk.word_tokenize(text)
		text_list += a
	# print(text_list)
	return text_list

def preProcess(lst):
	"""
	Remove all the punctuations and stop words 
	"""
	# english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
	# text_list = [word for word in lst if word not in english_punctuations]  # remove punctuations

	stops = set(stopwords.words("english")) 
	text_list = [word for word in lst if word not in stops]  # remove stope words
	#print(text_list)
	return text_list

def mostCommon(lst,x):
	"""
	Find the xK most frequent words in the document
	"""
	freq_dist = nltk.FreqDist(lst)
	mst_freq = freq_dist.most_common(x*100)

	return mst_freq


# main 
n = int(input("Please enter the 10K most frequent you want to find: "))
json_lst = readfile(filename)
words_lst = extractText(json_lst)
words_lst_pre = preProcess(words_lst)
wlst = mostCommon(words_lst_pre,n)
print(wlst)



import os,time
import threading

rlock = threading.RLock()
curPosition = 0

class Reader(threading.Thread):
    def __init__(self, res):
        self.res = res
        super(Reader, self).__init__()
    def run(self):
        fstream = open(self.res.fileName)
        global curPosition
        lst = []
        try:
            while True:
                #锁定共享资源
                rlock.acquire()
                startPosition = curPosition
                curPosition = endPosition = (startPosition + self.res.blockSize) if (startPosition + self.res.blockSize) < self.res.fileSize else self.res.fileSize
                #释放共享资源
                rlock.release()
                if startPosition == self.res.fileSize:
                    break
                elif startPosition != 0:
                    fstream.seek(startPosition)
                    fstream.readline() 

                pos = fstream.tell()
                while pos < endPosition:
                    line = fstream.readline()
                    pos = fstream.tell()
                    r = json.loads(line)
                    lst.append(r)
        except:
            return lst
            fstream.close()
        

        

class Resource(object):
    def __init__(self, fileName):
        self.fileName = fileName
        #分块大小
        self.blockSize = 100000
        self.getFileSize()
    #计算文件大小
    def getFileSize(self):
        fstream = open(self.fileName, 'r')
        fstream.seek(0, os.SEEK_END)
        self.fileSize = fstream.tell()
        fstream.close()

if __name__ == '__main__':
    starttime = time.process_time()
    #线程数
    threadNum = 4
    #文件
    fileName = '2014news1000.json';
    res = Resource(fileName)
    threads = []
    #初始化线程
    for i in range(threadNum):
        rdr = Reader(res)
        threads.append(rdr)
    #开始线程
    for i in range(threadNum):
        threads[i].start()
    #结束线程
    for i in range(threadNum):
        threads[i].join()

    print(time.process_time() - starttime)



