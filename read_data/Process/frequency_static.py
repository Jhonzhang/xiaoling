# encoding: utf-8
# import ConfigParser
import os
import mysql.connector
import re
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import read_data.config
import pynlpir
import codecs

from sklearn.feature_extraction.text import CountVectorizer

def grab_corpus(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'w')
    pickle.dump(input_corpus,fw)
    fw.close()

# def switch_fun(str_space):
#     if ' ' in str_space:


def frequency_fun(corpus):
    #统计corpus中的词频
    word_dic = {}
    for each_item_str in corpus:
        each_item_list = each_item_str.split()
        for each_word in each_item_list:
            if each_word not in word_dic:
                word_dic[each_word] = 1
            else:
                word_dic[each_word] +=1
    return word_dic

def write_txt(word_dic,store_filename):
    output = open(store_filename, 'w')
    for word in word_dic:

        word_cnt = word_dic[word]
        word = word.encode('utf-8')

        output.write(str(word))
        output.write('---')
        output.write(str(word_cnt))
        output.write('\n')
    output.close()


if __name__=='__main__':
    corpus_content = grab_corpus('content.txt')
    corpus_name = grab_corpus('title.txt')
    #print corpus_name[5]
    content_word_dic = frequency_fun(corpus_content)
    name_word_dic = frequency_fun(corpus_name)

    write_txt(content_word_dic,'content_dic.txt')
    write_txt(name_word_dic,'name_dic.txt')

    # vectorizer = CountVectorizer()
    # print vectorizer.fit_transform(corpus_content).todense()