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
import time

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

# [dic.doc2bow(text) for text in texts]

def post_tfidf(id_list,data_list):
    from sklearn.feature_extraction.text import HashingVectorizer
    #fr = open(url + "/post_key.txt", "r", encoding="utf8")
    # id_list = []
    # data_list = []
    # for line in fr.readlines():
    #     term = line.strip().split("\t")
    #     if len(term) == 2:
    #         id_list.append(term[0])
    #         data_list.append(term[1])

    hv = HashingVectorizer(n_features=10000, non_negative=True)  # 该类实现hash技巧
    post_tfidf = hv.fit_transform(data_list)  # return feature vector 'fea_train' [n_samples,n_features]
    print('Size of fea_train:' + repr(post_tfidf.shape))
    print(post_tfidf.nnz)
    post_cluster(id_list, post_tfidf)

def post_cluster(id, tfidf_vec):
    from sklearn.cluster import KMeans
    kmean = KMeans(n_clusters=300)
    print("kmeans", kmean.fit(tfidf_vec))
    #     pred = kmean.transform(tfidf_vec)

    count1 = 0
    count2 = 0
    #     pred_str = []
    #
    #     for item in pred:
    #         count1 += 1
    #         vec = ""
    #         for tmp in item :
    #             vec += str(tmp)[0:7] + "\t"
    #         pred_str.append(vec)
    #
    #     print len(pred_str)
    #     print len(id)

    pred = kmean.predict(tfidf_vec)
    fo = open( "cluster.txt","a+")
    for i in range(len(pred)):
        count2 += 1
        fo.write(id[i] + "\t" + str(pred[i]) + "\n")
    fo.close()
    print("%d+%d" % (count1, count2))


def post_lda(cluster,id_list,data_list_lis):
    from gensim import corpora, models, matutils
    count = 0
    #fr = open("post_key.txt", "r")
    fo2 = open("post_vec_lda.txt", "a+")
    id_list = id_list
    data_list = data_list_lis

    # for line in fr.readlines():
    #     term = line.strip().split("\t")
    #     if len(term) == 2:
    #         count += 1
    #         id_list.append(term[0])
    #         word = term[1].strip().split()
    #         data_list.append(word)
    print("lda")
    dic = corpora.Dictionary(data_list)  # 构造词典
    corpus = [dic.doc2bow(text) for text in data_list]  # 每个text 对应的稀疏向量
    tfidf = models.TfidfModel(corpus)  # 统计tfidf
    print("lda")
    corpus_tfidf = tfidf[corpus]  # 得到每个文本的tfidf向量，稀疏矩阵
    lda = models.LdaModel(corpus_tfidf, id2word=dic, num_topics=43)
    corpus_lda = lda[corpus_tfidf]  # 每个文本对应的LDA向量，稀疏的，元素值是隶属与对应序数类的权重
    print("lda")

    num = 0
    for doc in corpus_lda:
        wstr = ""
        for i in range(len(doc)):
            item = doc[i]
            wstr += str(item[0]) + "," + str(item[1])[0:7] + "/"
        fo2.write(id_list[num][0] + "\t" + wstr[0:-1] + "\n")
        num += 1
    # fr.close()
    fo2.close()
    print(num)

    if cluster:
        lda_csc_matrix = matutils.corpus2csc(corpus_lda).transpose()  # gensim sparse matrix to scipy sparse matrix
        post_cluster(id_list, lda_csc_matrix)


if __name__ == "__main__":
    #url = "Path"
    time_start = time.time()
    #post_cut
    corpus_content = grab_corpus('train_content')
    corpus_ids = grab_corpus('train_content.txt')

    id_list = corpus_ids
    data_list = corpus_content
    id_list_lis = switch_type(corpus_ids)
    texts = switch_type(corpus_content)
    # print type(data_list)
    # print data_list
    post_tfidf(id_list,data_list)
    lda_cluster = False
    post_lda(lda_cluster,id_list,texts)
    print  (time.time() - time_start)