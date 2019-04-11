# -*- coding: utf-8 -*-
import jieba.analyse
# import jieba
import warnings
from gensim.models import word2vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from numpy import shape
import os
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

def write_similar_with_txt_type(word,cluster_name,top_num,top_num_similar_items):
    path_dir =  r'D:/xiaoling/topic_detection/read_data/each_cluster_similar_words/'+cluster_name
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)

    file_name = path_dir +'/'+word+'-相似度前'+str(top_num)+'的.txt'
    fw = open(file_name,'a+')
    for items in top_num_similar_items :
    #     print(items[0],items[1])
    # for key,value in dic_tfidf.items():
        fw.write(items[0]+'--'+str(items[1]))
        fw.write('\n')

    fw.close()

def get_each_cluster_content():
    file_path = r'D:/xiaoling/topic_detection/read_data/Process/cluster_content_dic.txt'
    #file_path_by = bytes(file_path,encoding= 'utf-8')
    corpus_contents = grab_corpus(file_path)
    # print (type(corpus_contents))
    #print (len(corpus_contents))
    #print(corpus_contents.keys())
    all_keys_cluster_name = corpus_contents.keys()
    for each_cluster_name in all_keys_cluster_name:

      print (each_cluster_name,"类所含文档数量为：",len(corpus_contents[each_cluster_name]))
      compute_each_cluster_tfidf_value(corpus_contents[each_cluster_name],each_cluster_name)


def compute_each_cluster_tfidf_value(one_cluster_after_segment_corpus,cluster_name):

    #one_cluster_after_segment_corpus = get_each_cluster_content()
    # print(type(one_cluster_after_segment_corpus))
    print("*"*50)
    #print(one_cluster_after_segment_corpus)
    vectorizer = TfidfVectorizer(min_df=1, use_idf=True)

    X = vectorizer.fit_transform(one_cluster_after_segment_corpus)

    #return X, vectorizer

    #print(type(vectorizer.get_feature_names()),vectorizer.get_feature_names()) #获取词袋中所有文本关键词
    # 1 计算单词在文档中的频率
    #print("打印：：：：")
    #print (vectorizer.fit_transform(one_cluster_after_segment_corpus).todense())
    #print(X.toarray()) #对应的tfidf矩阵，每篇文档转换成词的个数表示
    #print (type(vectorizer.vocabulary_),vectorizer.vocabulary_)
    #print("#"*50,"所有词汇按词频降序输出")
    #print(sorted(vectorizer.vocabulary_.items(), key=lambda d: d[1],reverse=True)) #词频降序输出
    tfidf_arrry_mar = X.todense()
    #print('类型：',type(tfidf_arrry_mar))
    #print(len(tfidf_arrry_mar))
    #print ("行列数：",shape(tfidf_arrry_mar))
    #print(type(tfidf_arrry_mar[0]))
    #print("&"*80,"结果：")
    #print(len(tfidf_arrry_mar[0]+tfidf_arrry_mar[1]))

    sum_tfidf_mar_row = tfidf_arrry_mar.sum(axis =0)
    # print(shape(sum_tfidf_mar_row))
    # print(type(sum_tfidf_mar_row.tolist()[0]))
    # print(sum_tfidf_mar_row.tolist()[0])
    values_tfidf = sum_tfidf_mar_row.tolist()[0]
    keys_tfidf = vectorizer.get_feature_names()
    dictionary_tfidf = dict(zip(keys_tfidf,values_tfidf))
    #print (dictionary_tfidf)
    #print("降序输出")
    reverse_dictionary_tfidf =dict(sorted(dictionary_tfidf.items(),key=lambda x:x[1],reverse=True))
    #print(reverse_dictionary_tfidf)
    write_dict_with_txt_type(reverse_dictionary_tfidf, cluster_name)

    #print(sorted(vectorizer.vocabulary_.items(), key=lambda d: d[1], reverse=True))  # 词频降序输出

# def switch_type(corpus_content):
#     texts = []
#     for each_content in corpus_content:
#         each_content_list = each_content.split()
#         each_content_list = [tmp.lower() for tmp in each_content_list if len(tmp)>1]
#         texts.append(each_content_list)
#     return texts

def similar_top_words(cluster_name,word,top_num=10):
    file_path = r'D:/xiaoling/topic_detection/read_data/Process/cluster_content_dic.txt'
    # file_path_by = bytes(file_path,encoding= 'utf-8')
    corpus_contents = grab_corpus(file_path)
    cluster_content = corpus_contents[cluster_name]
    gensim_cluster_contents = switch_type(cluster_content)
    # 训练模型，部分参数如下
    model = word2vec.Word2Vec(gensim_cluster_contents, size=200, hs=1, min_count=1, window=3)
    # 与某个词（李达康）最相近的3个字的词
    print(u'与 '+word+' 最相近的'+str(top_num)+'个字的词')
    #req_count = top_num
    top_num_similar_items = model.wv.most_similar(word, topn=top_num)
    write_similar_with_txt_type(word, cluster_name, top_num,top_num_similar_items)
    # for items in top_num_similar_items :
    #     print(items[0],items[1])
    # for key in model.wv.similar_by_word(word, topn=top_num):
    #     if len(key[0]) == 3:
    #         req_count -= 1
    #         print(key[0], key[1])
    #         if req_count == 0:
    #             break

if __name__=='__main__':
    #计算每个类的TFIDF值
    #get_each_cluster_content()

    cluster_name = '经济管理' #每次运行前修改输入类别
    word = '米饭'
    top_num = 20
    #ont_cluster_contents = get_each_cluster_content(cluster_name)
    #运行一次输出
    #compute_each_cluster_tfidf_value()

    similar_top_words(cluster_name, word, top_num)
