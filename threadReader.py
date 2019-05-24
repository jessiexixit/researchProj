import time
# import configparser

import json
import nltk
import numpy as np
import re # remove digit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import threading

class Reader(threading.Thread):
    def __init__(self, file_name, start_pos, end_pos):
        super(Reader, self).__init__()
        self.file_name = file_name
        self.start_pos = start_pos
        self.end_pos = end_pos

    def run(self):
        fd = open(self.file_name, 'r')
        '''
        该if块主要判断分块后的文件块的首位置是不是行首，
        是行首的话，不做处理
        否则，将文件块的首位置定位到下一行的行首
        '''
        if self.start_pos != 0:
            fd.seek(self.start_pos-1)
            if fd.read(1) != '\n':
                line = fd.readline()
                self.start_pos = fd.tell()
        fd.seek(self.start_pos)
        '''
        对该文件块进行处理
        '''
        while (self.start_pos <= self.end_pos):
            line = fd.readline()

            '''
            do somthing
            '''
            self.start_pos = fd.tell()

'''
对文件进行分块，文件块的数量和线程数量一致
'''
class Partition(object):
    def __init__(self, file_name, thread_num):
        self.file_name = file_name
        self.block_num = thread_num

    def part(self):
        fd = open(self.file_name, 'r')
        fd.seek(0, 2)
        pos_list = []
        file_size = fd.tell()
        block_size = file_size/self.block_num
        start_pos = 0
        for i in range(self.block_num):
            if i == self.block_num-1:
                end_pos = file_size-1
                pos_list.append((start_pos, end_pos))
                break
            end_pos = start_pos+block_size-1
            if end_pos >= file_size:
                end_pos = file_size-1
            if start_pos >= file_size:
                break
            pos_list.append((start_pos, end_pos))
            start_pos = end_pos+1
        fd.close()
        return pos_list

if __name__ == '__main__':
    wd_lst = []
    map_f = open("mapper.txt", "w+")

    '''
    读取配置文件
    '''
    # config = ConfigParser.ConfigParser()
    # config.readfp(open("2014news1000.json"))
    # #文件名
    # file_name = config.get('info', 'fileName')
    file_name = "2014news1000.json"
    #线程数量
    # thread_num = int(config.get('info', 'threadNum'))
    thread_num = 4
    #起始时间
    # start_time = time.clock()
    p = Partition(file_name, thread_num)
    t = []
    pos = p.part()
    #生成线程
    for i in range(thread_num):
        t.append(Reader(file_name, *pos[i]))
    #开启线程
    for i in range(thread_num):
        line = t[i].start()
        if line:
            json_dic = json.loads(line) # generate dictionary one by one
            wd_lst = preProcess(json_dic)
            for i in wd_lst:    # write the after process word list into file mapper.txt
                map_f.write("{} {}\n".format(i,1))
                    # print("test 1")
        else:
            break

    for i in range(thread_num):
        t[i].join()
    #结束时间
    map_f.close()

    end_time = time.clock()
    # print ("Cost time is %f" % (end_time - start_time))