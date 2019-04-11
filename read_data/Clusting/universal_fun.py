# encoding: utf-8
# import ConfigParser
import os
import mysql.connector
import re
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import pynlpir
import codecs

def get_stop_word():
    stop_words = []
    st = codecs.open(r'D:\xiaoling\topic_detection\read_data\stopwords.txt', 'r', encoding='utf-8')
    for line in st:
        line = line.strip()
        # print line
        stop_words.append(line)
    return stop_words

def delete_stop_words(each_article_content):
    pynlpir.open()
    # 分词和去除停用词
    stop_words = get_stop_word()
    after_deal_content = ""
    segments = pynlpir.segment(each_article_content, pos_english=True, pos_tagging=True, pos_names=None)
    for segment in segments:
        # print segment[0],'\t',segment[1]
        # print segment[0]
        word = segment[0]
        word = word.strip()
        if word not in stop_words:
            if word >= u'\u4e00' and word <= u'\u9fa5':
              after_deal_content += (word + ' ')

    pynlpir.close()
    return after_deal_content

def switch_type(corpus_content):
    texts = []
    for each_content in corpus_content:
        each_content_list = each_content.split()
        each_content_list = [tmp.lower() for tmp in each_content_list if len(tmp)>1]
        texts.append(each_content_list)
    return texts