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
from  universal_fun import switch_type,delete_stop_words
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

from gensim import corpora, models, similarities
from pprint import pprint

def GenDictandCorpus():
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering",
                 "Graph minors A survey"]

    texts = [[word for word in document.lower().split()] for document in documents]

    # 词典
    dictionary = corpora.Dictionary(texts)
    # 词库，以(词，词频)方式存贮
    corpus = [dictionary.doc2bow(text) for text in texts]
    print(dictionary)
    print(corpus)
    return dictionary, corpus

def Tfidf():
    dictionary, corpus = GenDictandCorpus()

    # initialize a model
    tfidf = models.TfidfModel(corpus)
    # print(tfidf)

    # Transforming vectors
    # 此时，tfidf被视为一个只读对象，可以用于将任何向量从旧表示（词频）转换为新表示（TfIdf实值权重）
    doc_bow = [(0, 1), (1, 1)]
    # 使用模型tfidf，将doc_bow(由词,词频)表示转换成(词,tfidf)表示
    # print(tfidf[doc_bow])

    # 转换整个词库
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    return corpus_tfidf

def LDA():
    dictionary, corpus = GenDictandCorpus()
    corpus_tfidf = Tfidf()
    ldamodel = models.LdaModel(corpus, id2word=dictionary, num_topics=2)

    ldamodel.print_topics()
    pprint(ldamodel.print_topics())

# 潜在语义索引(Latent Semantic Indexing,以下简称LSI)，有的文章也叫Latent Semantic  Analysis（LSA）
# LSI是基于奇异值分解（SVD）的方法来得到文本的主题的
def LSI():
    dictionary, corpus = GenDictandCorpus()
    corpus_tfidf = Tfidf()

    # initialize an LSI transformation
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    corpus_lsi = lsi[corpus_tfidf]
   # print(corpus_lsi)
   # pprint(lsi.print_topics(2))
   # 在这里实际执行了bow-> tfidf和tfidf-> lsi转换
    for doc in corpus_lsi:
        print(doc)

    # lsi.save('/tmp/model.lsi')
    # lsi = models.LsiModel.load('/tmp/model.lsi')

# 随机投影(Random Projections)，RP旨在减少矢量空间维数。
# 这是非常有效的方法，通过投掷一点随机性来近似文档之间的TfIdf距离。
# 推荐的目标维度数百/千，取决于您的数据集。
def RP():
    corpus_tfidf = Tfidf()
    print("打印tiidf值：",corpus_tfidf)
    RP_model = models.RpModel(corpus_tfidf, num_topics=2)
   # print(RP_model)
    corpus_rp = RP_model[corpus_tfidf]
    for doc in corpus_rp:
        print(doc)

if __name__=='__main__':
    print ('测试打印','*'*30)
    #LDA()
    RP()
    #LSI()
