# encoding: utf-8
import ConfigParser
import os
import mysql.connector
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import read_data.config
import pynlpir
import codecs
import bs4
import nltk

class Process(object):
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

    def get_stop_word(self):
        stop_words = []
        st = codecs.open(r'D:\xiaoling\topic_detection\read_data\stopwords.txt', 'r', encoding='utf-8')
        for line in st:
            line = line.strip()
            # print line
            stop_words.append(line)
        return stop_words

    def delete_stop_words(self,each_article_content):
        pynlpir.open()
        #分词和去除停用词
        stop_words = self.get_stop_word()
        after_deal_content = ""
        segments = pynlpir.segment(each_article_content, pos_english=True, pos_tagging=True,pos_names=None)
        for segment in segments:
            # print segment[0],'\t',segment[1]
            # print segment[0]
            word = segment[0]
            word = word.strip()
            if word not in stop_words:
                if word >= u'\u4e00' and word <= u'\u9fa5':
                    after_deal_content += (word + '\t')

        pynlpir.close()
        return after_deal_content
    def just_splite_words(self,each_article_content):
        pynlpir.open()
        #分词和去除停用词

        after_deal_content = ""
        segments = pynlpir.segment(each_article_content, pos_english=True, pos_tagging=True,pos_names=None)
        for segment in segments:
            # print segment[0],'\t',segment[1]
            # print segment[0]
            word = segment[0]
            word = word.strip()

            if word >= u'\u4e00' and word <= u'\u9fa5':
                after_deal_content += (word + ' ')

        pynlpir.close()
        #print after_deal_content
        return after_deal_content

    def frequency_compute(self,corpus):
        pass

    def store_corpus(self,input_corpus,filename):
        import pickle
        fw =  open(filename,'w')
        pickle.dump(input_corpus,fw)
        fw.close()



    def datatransfromone(self):

        table_name = 'source_content_20181231'
        sql = "select id ,article_content,article_name,book_article_name from " + table_name
        self.cur.execute(sql)
        results = self.cur.fetchall()
        corpus_name = []
        corpus_content =[]
        for each_result in results:
           id = each_result[0]
           each_article_content = each_result[1]
           each_article_name = each_result[2]
           book_article_name = each_result[3]
           after_each_article_cotent = self.just_splite_words(each_article_content)
           corpus_content.append(after_each_article_cotent)

           after_each_article_name = self.just_splite_words(each_article_name)
           corpus_name.append(book_article_name)

           updateSql = "update  %s set fenci_content = '%s',fenci_name = '%s' where id = '%s'" % (str(table_name),str(after_each_article_cotent),str(after_each_article_name),id)

           self.cur.execute(updateSql)
           self.db.commit()

        return corpus_content,corpus_name


if __name__=='__main__':
    process_data = Process()
    #self.dbInit()
    process_data.dbInit()
    corpus_content,corpus_name = process_data.datatransfromone()
    process_data.store_corpus(corpus_content,'corpus_content.txt')
    process_data.store_corpus(corpus_name, 'corpus_name.txt')
    process_data.db_close()