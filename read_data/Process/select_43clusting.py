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
import re
import codecs

def read_fun(path):
    path = r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)"
    unicode_paths = str(path)

db = mysql.connector.connect(host=read_data.config.HOST, user=read_data.config.USER,
                                          password=read_data.config.PASSWORD, db=read_data.config.DB, charset="utf8")
        # self.db = MySQLdb.connect("127.0.0.1","root","","fits" ,charset="utf8")
cur = db.cursor()
def select_id_fun(path):
    table_name =  'source_content_20181231'
    sql = "select id ,article_content from " + table_name +" where book_article_name = '" +str(path)+"'"
    cur.execute(sql)
    results = cur.fetchone()
    #print "数据库结果：",results
    return  results

def grab_corpus(filename):
    import pickle
    fr = open(filename,'rb+')
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'wb+')
    pickle.dump(input_corpus,fw)
    fw.close()

def splite_words(each_article_content,stop_words):
    pynlpir.open()
        #分词和去除停用词

    after_deal_content = ""
    segments = pynlpir.segment(each_article_content, pos_english=True, pos_tagging=True,pos_names=None)

    for segment in segments:
            # print segment[0],'\t',segment[1]
            # print segment[0]
        word = segment[0]
        word = word.strip()
        if word not in stop_words:
            if word >= u'\u4e00' and word <= u'\u9fa5':
                after_deal_content += (word + ' ')

    pynlpir.close()
    #print after_deal_content
    return after_deal_content
def get_stop_word():
    stop_words = []
    st = codecs.open(r'D:\xiaoling\topic_detection\read_data\stopwords.txt', 'r', encoding='utf-8')
    for line in st:
        line = line.strip()
            # print line
        stop_words.append(line)
    return stop_words
path_file = r"C:\Users\ztf\Desktop\3392个文本以及标题-类别的标注\标题-类别（3392文本的二级话题）.txt"

unicode_paths =str(path_file)
f = open(unicode_paths,'r+',encoding='utf-8')
cluster_path_dic = {}
cluster_id_dic = {}
cluster_content_dic = {}
line = f.readline()
train_ids = []
train_targets = []
train_content = []
i= 0
stop_words = get_stop_word()
while line:
    #print line
    line_item = line.split('t-')
    path = line_item[0]+'t'
    print (i,"原始路径：",path)
    path = path.replace('\\', r'\\').replace(' ','')
    print(path)
    cluster = line_item[1]
    cluster = cluster.strip('\n').strip('\t').strip(' ')
    results= select_id_fun(path)
    print ("返回的长度：",len(results))
    id = results[0]
    each_article_content = results[1]
    train_ids.append(str(id))
    train_targets.append(cluster)
    after_each_article_cotent = splite_words(each_article_content,stop_words)
    train_content.append(after_each_article_cotent)
    if cluster not in cluster_path_dic:
        # tmp_path_list = []
        # tmp_id_list = []
        # tmp_content_list = []
        cluster_path_dic[cluster] = []
        cluster_id_dic[cluster] = []
        cluster_content_dic[cluster] = []
        cluster_path_dic[cluster].append(path)
        cluster_id_dic[cluster].append(str(id))
        cluster_content_dic[cluster].append(after_each_article_cotent)
    else:
        cluster_path_dic[cluster].append(path)
        cluster_id_dic[cluster].append(str(id))
        cluster_content_dic[cluster].append(after_each_article_cotent)
    line = f.readline()
    i = i+1
f.close()

store_corpus(train_ids,' train_ids_list.txt')
store_corpus(train_targets,'train_targets_list.txt')
store_corpus(train_content,'train_content_list.txt')
store_corpus(cluster_path_dic,'cluster_path_dic.txt')
store_corpus(cluster_id_dic,'cluster_id_dic.txt')
store_corpus(cluster_content_dic,'cluster_content_dic.txt')
# print [x for x in cluster_path_dic.keys()]
db.commit()
cur.close()
db.close()

for key in cluster_id_dic.keys():
    print (key,cluster_id_dic[key])