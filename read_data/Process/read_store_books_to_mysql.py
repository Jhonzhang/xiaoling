#-*- coding: utf-8 -*-

import os
import codecs
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import re
import mysql.connector
import read_data.config
import chardet

class Store(object):
    def dbInit(self):
        # print "dbInit"
        self.db = mysql.connector.connect(host=read_data.config.HOST, user=read_data.config.USER,
                                          password=read_data.config.PASSWORD, db=read_data.config.DB, charset="utf8")
        # self.db = MySQLdb.connect("127.0.0.1","root","","fits" ,charset="utf8")
        self.cur = self.db.cursor()
        #self.r = re.compile(r'charset=(.+)"')

    def __init__(self):
        path = r"C:\Users\99355\Desktop\3392个文本以及标题-类别的标注\3392个文本"
        #unicode_paths = unicode(path, "utf-8")
        self.source_path = str(path)

    def db_close(self):
        self.db.commit()
        self.cur.close()
        self.db.close()

    def switch_type(self,cont):
        cont = cont.strip()
        cont = cont.replace("\n", "")
        if len(cont) != 0:
            char_type = chardet.detect(cont)['encoding']
            # new_cont = unicode(cont)
            print ("编码类型：", char_type)
            if char_type == "GB2312":
                char_type = "gbk"
            elif char_type == None:
                char_type = "utf-8"
                # cont = unicode(cont)
            elif char_type != "utf-8" and char_type != "ascii":
                char_type = "gbk"
                # new_cont = cont.decode(char_type, 'ignore').encode('utf-8')
                # cont = unicode(cont)

            new_cont = cont.decode(char_type, 'ignore').encode('utf-8')

        else:
            new_cont = ""

        return new_cont

    def read_each_article(self,path):
        info = open(path, 'rb')
        # path = unicode(path, "utf-8")
        absolute_path = path.split(self.source_path)
        book_article_name = absolute_path[1]
        article_list = info.readlines()
        if len(article_list) > 0:
            article_name = article_list[0]
            article_name = self.switch_type(article_name)
            auther = article_list[1]
            auther = self.switch_type(auther)
            source = article_list[2]
            source = self.switch_type(source)
            if len(article_list) > 3:
                content = article_list[3:]
                # print "正文：", type(article_list[2:])
                article_content = ''.join(content)
                char_type = chardet.detect(article_content)['encoding']
                if char_type == "GB2312":
                    char_type = "gbk"
                article_content = article_content.decode(char_type, 'ignore').encode('utf-8')

            else:
                article_content = ""
            # print "文章名称：",article_content
            content_table_name = "source_content_20181231"
            l = [str(book_article_name), str(auther), str(source), str(article_name), str(article_content)]
            sql = 'insert ignore into ' + content_table_name + '(book_article_name,auther,source,article_name,article_content) values(%s, %s, %s, %s, %s)'
            try:
                self.cur.execute(sql, l)
                self.db.commit()

                # print 'update success'
            except Exception as e:
                print ('Error:', e)

        info.close()

    def read_files(self,path):

        if (os.path.exists(path) and os.path.isdir(path)):
            #如果该路径不存在，则报错。
            files = os.listdir(path)
            if len(files)>=1:
                for each_parent_file_name in files:
                    if '.bat' not in each_parent_file_name:

                        #print "*" * 3, each_parent_file_name
                        each_parent_file_path = os.path.join(path, each_parent_file_name)
                        if (os.path.isdir(each_parent_file_path)):
                            #下一级目录仍旧是文件夹，则返回当前路径，以及所有文件夹名称。
                            return [1,path,files]
                        else:
                            article_names = files
                            return [0,path,article_names]
                    else:
                        continue
            else:
                return [2]

        else:
            return [2]

    def read_articls(self,all_articles,final_article_path):
        for each_article_name in all_articles:
            if ".txt" in each_article_name:
                each_article_path = os.path.join(final_article_path,each_article_name)
                # print each_article_path
                self.read_each_article(each_article_path)
                # info = open(each_article_path, 'r')
                # print "文章内容：",len(info.read())
                # info.close()


    def read_and_store_files(slef,unicode_paths):
        #读入路径，处理文本并存储
        back = slef.read_files(unicode_paths)
        #print "检测",back
        print ("标志：",back[0])
        #back[0]，1表示还有下一级目录，0 表示没有
        flag= back[0]
        if flag == 1:
            back_path = back[1] #路径名
            back_files = back[2]#文件夹名
            for each_file_name in back_files:
                #对文件夹下循环调用read_and_store_files()函数
                if '.bat' not in each_file_name:
                    print  ("now file name:","*" * 7, each_file_name)
                    each_file_path = os.path.join(back_path, each_file_name)
                    slef.read_and_store_files(each_file_path)
        elif flag ==0:
            #说明已经处理到文档部分，下一层没有文件夹了。
            all_articles = back[2]
            final_article_path = back[1]
            slef.read_articls(all_articles,final_article_path)
        else:
            pass



if __name__=='__main__':
    store_data = Store()
    #self.dbInit()
    store_data.dbInit()
    #path = r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)"
    #unicode_paths = unicode(path, "utf-8")
    unicode_paths = store_data.source_path
    #print "路径：", unicode_paths
    store_data.read_and_store_files(unicode_paths)
    store_data.db_close()
