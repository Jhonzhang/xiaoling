# encoding: utf-8
# import ConfigParser
import os
import mysql.connector
import re
# import sys
# # reload(sys)
# sys.setdefaultencoding("utf-8")
import read_data.config
import pynlpir
import codecs

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import gensim
# sys.path.append(r'D:\xiaoling\topic_detection\read_data\Process\preprocess_data.py')
# from .Process.preprocess_data import
# from read_data.Process.preprocess_data import Process.delete_stop_words
from gensim import corpora, models, similarities


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

raw_documents = [
    '无偿居间介绍买卖毒品的行为应如何定性',
    '吸毒男动态持有大量毒品的行为该如何认定',
    '如何区分是非法种植毒品原植物罪还是非法制造毒品罪',
    '为毒贩贩卖毒品提供帮助构成贩卖毒品罪',
    '将自己吸食的毒品原价转让给朋友吸食的行为该如何认定',
    '为获报酬帮人购买毒品的行为该如何认定',
    '毒贩出狱后再次够买毒品途中被抓的行为认定',
    '虚夸毒品功效劝人吸食毒品的行为该如何认定',
    '妻子下落不明丈夫又与他人登记结婚是否为无效婚姻',
    '一方未签字办理的结婚登记是否有效',
    '夫妻双方1990年按农村习俗举办婚礼没有结婚证 一方可否起诉离婚',
    '结婚前对方父母出资购买的住房写我们二人的名字有效吗',
    '身份证被别人冒用无法登记结婚怎么办？',
    '同居后又与他人登记结婚是否构成重婚罪',
    '未办登记只举办结婚仪式可起诉离婚吗',
    '同居多年未办理结婚登记，是否可以向法院起诉要求离婚'
]
corpora_documents_old = []
for item_text in raw_documents:
    item_str =delete_stop_words(item_text)
    corpora_documents_old.append(item_str)

def switch_type(corpus_content):
    texts = []
    for each_content in corpus_content:
        each_content_list = each_content.split()
        each_content_list = [tmp.lower() for tmp in each_content_list if len(tmp)>1]
        texts.append(each_content_list)
    return texts

corpora_documents = switch_type(corpora_documents_old)
print (len(corpora_documents))
# 判断关键字的相似度
print (corpora_documents_old)
print ('+-'*50)
# corpora_documents = corpora_documents_old
model = gensim.models.word2vec.Word2Vec(corpora_documents, size=1000)
print(model.most_similar(u'毒品', topn=10))
key = model.most_similar(u'毒品', topn=10)
for each in key:
    print (each[0])
print  ('*'*50)
dictionary = corpora.Dictionary(corpora_documents)
print(dictionary)
corpus = [dictionary.doc2bow(text) for text in corpora_documents]
print(corpus)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# 根据结果使用lsi做主题分类效果会比较好
print('#############' * 4)
lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
lsi.print_topics(2)
for doc in corpus_lsi:
    print(doc)

print('#############' * 4)
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2, update_every=0, passes=1)
corpus_lda = lda[corpus_tfidf]
lda.print_topics(2)
for doc in corpus_lda:
    print(doc)
