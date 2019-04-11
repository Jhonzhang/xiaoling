# -*- coding: utf-8 -*-
import jieba.analyse
import jieba
import warnings
from gensim.models import word2vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from numpy import shape
def grab_corpus(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

def store_corpus(input_corpus,filename):
    import pickle
    fw =  open(filename,'wb')
    pickle.dump(input_corpus,fw)
    fw.close()

def switch_type(corpus_content):
    texts = []
    for each_content in corpus_content:
        each_content_list = each_content.split(' ')
        each_content_list = [tmp.lower() for tmp in each_content_list]
        texts.append(each_content_list)
    return texts

def write_dict_with_txt_type(dic_tfidf,cluster_name):
    file_name = r'D:/xiaoling/topic_detection/read_data/each_cluster_TFIDF_values/'+cluster_name+'TFIDF值降序.txt'
    fw = open(file_name,'a+')
    # keys=
    # values
    # for index in range(len(dic_tfidf)):
    #     #each_line =
    #     fw.write(dic_tfidf.keys()[index]+"--"+dic_tfidf.values()[index])
    #     fw.write('\n')
    for key,value in dic_tfidf.items():
        fw.write(key+'--'+str(value))
        fw.write('\n')

    fw.close()





def get_each_cluster_content(cluster_name):
    file_path = r'D:/xiaoling/topic_detection/read_data/Process/cluster_content_dic.txt'
    #file_path_by = bytes(file_path,encoding= 'utf-8')
    corpus_contents = grab_corpus(file_path)
    # print (type(corpus_contents))
    #print (len(corpus_contents))
    #print(corpus_contents.keys())
    print (cluster_name,"类所含文档数量为：",len(corpus_contents[cluster_name]))
    #pass
    return corpus_contents[cluster_name]

#计算每个类的TFIDF
"""
 输入：类别
 输出：降序输出所有词的TFIDF值
"""
def compute_each_cluster_tfidf_value(cluster_name):
    n_features = 1000 #每文档表示的最大维数
    one_cluster_after_segment_corpus = get_each_cluster_content(cluster_name)
    # print(type(one_cluster_after_segment_corpus))
    print("*"*50)
    #print(one_cluster_after_segment_corpus)
    vectorizer = TfidfVectorizer(min_df=1, use_idf=True)

    X = vectorizer.fit_transform(one_cluster_after_segment_corpus)

    #return X, vectorizer

    #print(type(vectorizer.get_feature_names()),vectorizer.get_feature_names()) #获取词袋中所有文本关键词
    # 1 计算单词在文档中的频率
    print("打印：：：：")
    #print (vectorizer.fit_transform(one_cluster_after_segment_corpus).todense())
    #print(X.toarray()) #对应的tfidf矩阵，每篇文档转换成词的个数表示
    #print (type(vectorizer.vocabulary_),vectorizer.vocabulary_)
    print("#"*50,"所有词汇按词频降序输出")
    #print(sorted(vectorizer.vocabulary_.items(), key=lambda d: d[1],reverse=True)) #词频降序输出
    tfidf_arrry_mar = X.todense()
    #print('类型：',type(tfidf_arrry_mar))
    #print(len(tfidf_arrry_mar))
    print ("行列数：",shape(tfidf_arrry_mar))
    print(type(tfidf_arrry_mar[0]))
    print("&"*80,"结果：")
    print(len(tfidf_arrry_mar[0]+tfidf_arrry_mar[1]))

    sum_tfidf_mar_row = tfidf_arrry_mar.sum(axis =0)
    # print(shape(sum_tfidf_mar_row))
    # print(type(sum_tfidf_mar_row.tolist()[0]))
    # print(sum_tfidf_mar_row.tolist()[0])
    values_tfidf = sum_tfidf_mar_row.tolist()[0]
    keys_tfidf = vectorizer.get_feature_names()
    dictionary_tfidf = dict(zip(keys_tfidf,values_tfidf))
    #print (dictionary_tfidf)
    print("降序输出")
    reverse_dictionary_tfidf =dict(sorted(dictionary_tfidf.items(),key=lambda x:x[1],reverse=True))
    #print(reverse_dictionary_tfidf)
    write_dict_with_txt_type(reverse_dictionary_tfidf, cluster_name)

    #print(sorted(vectorizer.vocabulary_.items(), key=lambda d: d[1], reverse=True))  # 词频降序输出


# sentences = word2vec.Text8Corpus('C:/Users/ztf/Desktop/in_the_name_of_people_segment.txt')
#
# # 训练模型，部分参数如下

# model = word2vec.Word2Vec(sentences, size=100, hs=1, min_count=1, window=3)
# #
# # # 模型的预测
# # print('-----------------分割线----------------------------')
# #
# # # 计算两个词向量的相似度
# try:
#     sim1 = model.wv.similarity(u'沙瑞金', u'高育良')
#     sim2 = model.wv.similarity(u'李达康', u'易学习')
# except KeyError:
#     sim1 = 0
#     sim2 = 0
# print(u'沙瑞金 和 高育良 的相似度为 ', sim1)
# print(u'李达康 和 易学习 的相似度为 ', sim2)
# #
# print('-----------------分割线 1---------------------------')
# # 与某个词（李达康）最相近的3个字的词
# print(u'与李达康最相近的3个字的词')
# req_count = 5
# for key in model.wv.similar_by_word(u'李达康', topn=100):
#     if len(key[0]) == 3:
#         req_count -= 1
#         print(key[0], key[1])
#         if req_count == 0:
#             break
# #
# print('-----------------分割线 2---------------------------')
# # 计算某个词(侯亮平)的相关列表
# try:
#     sim3 = model.wv.most_similar(u'侯亮平', topn=20)
#     print(u'和 侯亮平 与相关的词有：\n')
#     for key in sim3:
#         print(key[0], key[1])
# except:
#     print(' error')
# #
# print('-----------------分割线 3 ---------------------------')
# # 找出不同类的词
# sim4 = model.wv.doesnt_match(u'沙瑞金 高育良 李达康 刘庆祝'.split())
# print(u'这类人物中不同类的人名', sim4)
#
# print('-----------------分割线 4---------------------------')
# # 保留模型，方便重用
# model.save(u'人民的名义.model')

if __name__=='__main__':
    cluster_name = '个人生活' #每次运行前修改输入类别
    #ont_cluster_contents = get_each_cluster_content(cluster_name)
    #运行一次输出
    compute_each_cluster_tfidf_value(cluster_name)
