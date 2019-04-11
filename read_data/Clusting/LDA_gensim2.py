# encoding: utf-8
#from __future__ import print_function
import re
# import sys
# import importlib
# importlib.reload(sys)
# sys.setdefaultencoding('utf8')
import read_data.config
import pynlpir
import codecs
# import ConfigParser
import os
import mysql.connector

import codecs
from sklearn import feature_extraction
import mpld3
#import gensim

import numpy as np
# import lda
# import lda.datasets
from gensim import corpora, models

# from python_zhongwenjulei import delete_stop_words,switch_type
from  universal_fun import switch_type,delete_stop_words
raw_documents = [
    '美国教练坦言，没输给中国女排，是输给了郎平',
    '美国无缘四强，听听主教练的评价',
    '中国女排晋级世锦赛四强，全面解析主教练郎平的执教艺术',
    '为什么越来越多的人买MPV，而放弃SUV？跑一趟长途就知道了',
    '跑了长途才知道，SUV和轿车之间的差距',
    '家用的轿车买什么好']

print(len(raw_documents))
corpora_documents_old = []
for item_text in raw_documents:
    item_str =delete_stop_words(item_text)
    corpora_documents_old.append(item_str)

corpora_documents = switch_type(corpora_documents_old)
print(len(corpora_documents))
# 判断关键字的相似度
# print corpora_documents_old
print('+-'*50)
dictionary = corpora.Dictionary(corpora_documents)
print(dictionary)
corpus = [dictionary.doc2bow(text) for text in corpora_documents]
print(corpus)
# 打印所有主题，每个主题显示4个词
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2)
for topic in lda.print_topics(num_words=4):
    print(topic)
# 主题推断
print(lda.inference(corpus))

print ("=====>>主题推断值<<======")
for e, values in enumerate(lda.inference(corpus)[0]):
    each_doc = corpora_documents[e]
    #each_docs = [ i.decode("unicode-escape")  for i in each_doc]
    print (each_doc[0])
    for ee, value in enumerate(values):
        print('\t主题%d推断值%.2f' % (ee, value))

# document-term matrix
# X = lda.datasets.load_reuters()
# print("type(X): {}".format(type(X)))
# print("shape: {}\n".format(X.shape))
# print(X[:5, :5])
#
# # the vocab
# vocab = lda.datasets.load_reuters_vocab()
# print("type(vocab): {}".format(type(vocab)))
# print("len(vocab): {}\n".format(len(vocab)))
# print(vocab[:5])
#
# # titles for each story
# titles = lda.datasets.load_reuters_titles()
# print("type(titles): {}".format(type(titles)))
# print("len(titles): {}\n".format(len(titles)))
# print(titles[:5])
#
# doc_id = 0
# word_id = 3117
# print("doc id: {} word id: {}".format(doc_id, word_id))
# print("-- count: {}".format(X[doc_id, word_id]))
# print("-- word : {}".format(vocab[word_id]))
# print("-- doc  : {}".format(titles[doc_id]))
#
# model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
# model.fit(X)
#
# topic_word = model.topic_word_
# print("type(topic_word): {}".format(type(topic_word)))
# print("shape: {}".format(topic_word.shape))
# print(vocab[:3])
# print(topic_word[:, :3])
#
# for n in range(5):
#     sum_pr = sum(topic_word[n, :])
#     print("topic: {} sum: {}".format(n, sum_pr))
#
# print '*'*70 #分割线
# n = 5
# for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
#     print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
#
# print '+-+'*50#输出文档-主题（Document-Topic）分布
# doc_topic = model.doc_topic_
# print("type(doc_topic): {}".format(type(doc_topic)))
# print("shape: {}".format(doc_topic.shape))
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     print("doc: {} topic: {}".format(n, topic_most_pr))
#
# print'#'*60#计算各个主题中单词权重分布的情况
#
# import matplotlib.pyplot as plt
#
# f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)
# for i, k in enumerate([0, 5, 9, 14, 19]):
#     ax[i].stem(topic_word[k, :], linefmt='b-',
#                markerfmt='bo', basefmt='w-')
#     ax[i].set_xlim(-50, 4350)
#     ax[i].set_ylim(0, 0.08)
#     ax[i].set_ylabel("Prob")
#     ax[i].set_title("topic {}".format(k))
#
# ax[4].set_xlabel("word")
#
# plt.tight_layout()
#
# print '@2'*50#第二种作图分析单词权重分布
#
# import matplotlib.pyplot as plt
#
# f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)
# for i, k in enumerate([1, 3, 4, 8, 9]):
#     ax[i].stem(doc_topic[k, :], linefmt='r-',
#                markerfmt='ro', basefmt='w-')
#     ax[i].set_xlim(-1, 21)
#     ax[i].set_ylim(0, 1)
#     ax[i].set_ylabel("Prob")
#     ax[i].set_title("Document {}".format(k))
#
# ax[4].set_xlabel("Topic")
#
# plt.tight_layout()
# plt.show()
