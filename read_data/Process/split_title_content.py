#-*- coding: utf-8 -*-
import os
import sys
import chardet
# reload(sys)
# sys.setdefaultencoding('utf-8')

path = r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)"


unicode_paths = str(path)
#print "路径：", unicode_paths
p =r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)\体验汉语写作教程初级1 陈作宏 邓秀均 11\15\15.1txt"
p_unicode_paths = str(p)

# s= p_unicode_paths.split(unicode_paths)
# print s[1]

paths = r"F:\topic_detection\read_data\1.2.txt"
info = open(paths, 'rb')
article_lists = info.readlines()
article_list =article_lists[1]
print (type(article_list))
article_list = article_list.replace("\n"",""").strip()
article_list = article_list.replace("\r"",""")
print (article_list,len(article_list))
print ("字符长度：",article_list)
ch_type = chardet.detect(article_list[0:])['encoding']
print (ch_type)
print ("文章名：",article_list.decode(ch_type,'ignore'))
# print "作者：",article_list[1]
# content = article_list[2:]
# print "正文：",type(article_list[2:])
# content = ''.join(content)
#print content.encode('utf-8')
#print len(info.readlines())
info.close()