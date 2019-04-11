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
import logging

def grab_corpus(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'w')
    pickle.dump(input_corpus,fw)
    fw.close()

corpus_content = grab_corpus('train_content')
#corpus_name = grab_corpus('title.txt')
#print "类型",type(corpus_content)
#print corpus_content[3]
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

def transform(corpus_content,n_features =1000):

    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2,use_idf=True)

    X = vectorizer.fit_transform(corpus_content)

    return X,vectorizer
    # 1 计算单词在文档中的频率
    #print vectorizer.fit_transform(corpus_content).todense()
    #print vectorizer.get_feature_names()
    #print type(vectorizer.vocabulary_),vectorizer.vocabulary_

    #real_vec = vectorizer.fit_transform(corpus_content)

    # logging.info(vectorizer.idf_)  # 特征对应的权重
    # logging.info(vectorizer.get_feature_names())  # 特征词
    # logging.info(real_vec.toarray())  # #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

def train(X,vectorizer,true_k=43,minibatch = False,showLable = False):
    #使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=10,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print ("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print (vectorizer.get_stop_words())
        for i in range(true_k):
            print  ("Cluster %d:" % i)
            for ind in order_centroids[i, :50]:
                print (' %s ' % terms[ind],'、',)
            print()
    result = list(km.predict(X))
    print ('Cluster distribution:')
    print (dict([(i, result.count(i)) for i in result]))
    return -km.score(X)

def test():
    '''测试选择最优参数'''
    dataset = corpus_content
    print ("%d documents" % len(dataset))
    X,vectorizer = transform(dataset,n_features=500)
    true_ks = []
    scores = []
    for i in range(3,80,1):
        score = train(X,vectorizer,true_k=i)/len(dataset)
        print (i,score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8,4))
    plt.plot(true_ks,scores,label="error",color="red",linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()

def out():
    '''在最优参数下输出聚类结果'''
    dataset = corpus_content
    X,vectorizer = transform(dataset,n_features=500)
    score = train(X,vectorizer,true_k=10,showLable=True)/len(dataset)
    print (score)
#test()

if __name__=='__main__':
    test()
    #out()
