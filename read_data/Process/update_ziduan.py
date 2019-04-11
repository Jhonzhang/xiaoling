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
import re

def read_fun(path):
    #path = r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - 格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)"
    unicode_paths = unicode(path, "utf-8")

db = mysql.connector.connect(host=read_data.config.HOST, user=read_data.config.USER,
                                          password=read_data.config.PASSWORD, db=read_data.config.DB, charset="utf8")
        # self.db = MySQLdb.connect("127.0.0.1","root","","fits" ,charset="utf8")
cur = db.cursor()

table_name =  'source_content'
sql = "select id ,book_article_name  from " + table_name
cur.execute(sql)
results = cur.fetchall()

for each_result in results:
    #print
    id = each_result[0]
    book_article_name = each_result[1]

    print "原始路径：", book_article_name
    book_article_name_new = book_article_name.replace('\\', r'\\').replace(' ','')

    updateSql = "update  %s set book_article_name = '%s' where id = '%s'" % (
    str(table_name), str(book_article_name_new), id)

    cur.execute(updateSql)
    db.commit()


db.commit()
cur.close()
db.close()