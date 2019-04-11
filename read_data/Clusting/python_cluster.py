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
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from dateutil import *
#import jieba
import matplotlib.pyplot as plt


def grab_corpus(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'w')
    pickle.dump(input_corpus,fw)
    fw.close()


def switch_type(corpus_content):
    texts = []
    for each_content in corpus_content:
        each_content_list = each_content.split(' ')
        each_content_list = [tmp.lower() for tmp in each_content_list]
        texts.append(each_content_list)
    return texts


if __name__ == "__main__":
    corpus_content = grab_corpus('train_content')
    corpus_ids = grab_corpus('train_content.txt')

    from sklearn import feature_extraction
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus_content))

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()

    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()

    # resName = "BaiduTfidf_Result.txt"
    # result = codecs.open(resName, 'w', 'utf-8')
    # for j in range(len(word)):
    #     result.write(word[j] + ' ')
    # result.write('\r\n\r\n')
    #
    # # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    # for i in range(len(weight)):
    #     print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    #     for j in range(len(word)):
    #         result.write(str(weight[i][j]) + ' ')
    print  ('Start Kmeans:')
    from sklearn.cluster import KMeans

    clf = KMeans(n_clusters=20)
    s = clf.fit(weight)
    print (s)

    # 20个中心点
    print ("打印出每个类的中心",(clf.cluster_centers_))

    # 每个样本所属的簇
    print ("打印出每个类的中心",(clf.labels_))
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        i = i + 1

    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print("inertia: {}".format(clf.inertia_))
    #print(clf.inertia_)

    '''
        6、可视化
    '''

    # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(weight)

    x = []
    y = []

    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    plt.scatter(x, y, c=clf.labels_, marker="x")
    plt.xticks(())
    plt.yticks(())
    plt.show()
    #plt.savefig('./sample.png', aspect=1)







