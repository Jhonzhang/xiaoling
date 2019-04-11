# encoding: utf-8
# import ConfigParser
import os
import mysql.connector
import re
import sys
#reload(sys)
sys.setdefaultencoding("utf-8")
import read_data.config
import pynlpir
import codecs
# from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans


class Cluster(object):
    def dbInit(self):
        # print "dbInit"
        self.db = mysql.connector.connect(host=read_data.config.HOST, user=read_data.config.USER,
                                          password=read_data.config.PASSWORD, db=read_data.config.DB, charset="utf8")
        # self.db = MySQLdb.connect("127.0.0.1","root","","fits" ,charset="utf8")
        self.cur = self.db.cursor()
        # self.r = re.compile(r'charset=(.+)"')

    def __init__(self):
        pass
        # path = r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)"
        # # unicode_paths = unicode(path, "utf-8")
        # self.source_path = unicode(path, "utf-8")

    def db_close(self):
        self.db.commit()
        self.cur.close()
        self.db.close()


    def switch(self,str):
        each_article_list = []
        spl_str = str.split('\t')
        print  ("类型：", type(spl_str))
        for each_word in spl_str:
            if len(each_word)>1:
                each_article_list.append(each_word)

        return each_article_list

    def s_lower(self, str):
        all_str = ""
        spl_str = str.split('\t')
        #print "类型：", type(spl_str)
        for each_word in spl_str:
            each_word = each_word.lower()
            all_str += each_word+" "
        return all_str

    def load_database(self):
        #加载数据
        table_name = 'source_content'
        sql = "select id ,fenci_content from " + table_name
        self.cur.execute(sql)
        results = self.cur.fetchall()
        dataset = []
        tagset = []
        for each_result in results:
            id = each_result[0]
            each_article_content = each_result[1]
            each_article_content = each_article_content.encode('utf-8')
            #print type(each_article_content)
            tagset.append(id)
            #after_deal_each_article_content = self.switch(each_article_content)
            dataset.append(each_article_content)
        print (len(dataset))
        return dataset,tagset

    def transform(self,dataset, n_features=1000):
        vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
        X = vectorizer.fit_transform(dataset)
        return X, vectorizer



    def train(self,X, vectorizer, true_k=10, minibatch=False, showLable=False):
        # 使用采样数据还是原始数据训练k-means，
        if minibatch:
            km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
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
                for ind in order_centroids[i, :10]:
                    print ( ' %s' % terms[ind])
                    #print()
            result = list(km.predict(X))
            print  ('Cluster distribution:')
            print  (dict([(i, result.count(i)) for i in result]))
            return -km.score(X)

    def test(self):
        '''测试选择最优参数'''
        dataset,tagset = self.load_database()
        print ( "%d documents" % len(dataset))
        X, vectorizer = self.transform(dataset, n_features=500)
        true_ks = []
        scores = []
        for i in range(10, 80, 100):
            value = self.train(X, vectorizer, true_k=i)
            print ("此时的值：",value)
            score = value / len(dataset)
            print (i, score)
            true_ks.append(i)
            scores.append(score)
        plt.figure(figsize=(8, 4))
        plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
        plt.xlabel("n_features")
        plt.ylabel("error")
        plt.legend()
        plt.show()

    def out(self):
        '''在最优参数下输出聚类结果'''
        dataset,tagset = self.load_database()
        print (len(dataset))
        X, vectorizer = self.transform(dataset, n_features=1000)
        score = self.train(X, vectorizer, true_k=20, showLable=True) / len(dataset)
        print (score)

    # test()
    # out()

    def cluster(self):

        table_name = 'source_content'
        sql = "select id ,fenci_content from " + table_name
        self.cur.execute(sql)
        results = self.cur.fetchall()

        for each_result in results:
           id = each_result[0]
           each_article_content = each_result[1]
           after_each_article_cotent = self.delete_stop_words(each_article_content)
           updateSql = "update  %s set fenci_content = '%s' where id = '%s'" % (str(table_name),str(after_each_article_cotent),id)

           self.cur.execute(updateSql)
           self.db.commit()



if __name__=='__main__':
    clust_data = Cluster()
    #self.dbInit()
    clust_data.dbInit()
    #clust_data.test()
    clust_data.out()
    clust_data.db_close()