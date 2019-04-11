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
corpus_ids = grab_corpus('train_content.txt')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
# corpus = [res1,res2,res3]
cntVector = CountVectorizer()
cntTf = cntVector.fit_transform(corpus_content)
print (cntTf)

lda = LatentDirichletAllocation(n_topics=43,
                                learning_offset=50.,
                                random_state=0)
docres = lda.fit_transform(cntTf)

print (docres)
print  (lda.components_)

