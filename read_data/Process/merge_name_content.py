# encoding: utf-8
# import ConfigParser
import os
import mysql.connector
import re
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import read_data.config
import pynlpir
import codecs

def grab_corpus(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'w')
    pickle.dump(input_corpus,fw)
    fw.close()



if __name__=='__main__':

    corpus_content = grab_corpus(r'D:\xiaoling\topic_detection\read_data\Process\train_targets_list.txt')
    print (len(corpus_content))
    corpus_name = grab_corpus(r'D:\xiaoling\topic_detection\read_data\Process\cluster_content_dic.txt')
    print (len(corpus_name))
    #print len(corpus_name['计划与未来'])
    for each_cluster in corpus_name.keys():
        each_cluster = each_cluster.strip('\n').strip('\t')
        print (each_cluster)
    # corpus_namess = grab_corpus(r'D:\xiaoling\topic_detection\read_data\Process\train_targets_list.txt')
    # print len(corpus_namess),len(set(corpus_namess))
    # j = 1
    # for i in corpus_namess:
    #     print j,i
    #     j= j+1