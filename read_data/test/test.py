#-*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
all_file_num = 0

# paths =r'C:\Users\Administrator\Desktop\1325'
# # paths1 =unicode(paths,'utf8')
# # pathsss = paths1.encode('gbk')
# filesss = os.listdir(paths)
# print filesss
def read_each_article(path):
    info = open(path, 'r')
    print info.readlines
    info.close()

def print_path(path):
   all_article_list= []
   #print "调用该程序"
   if(os.path.exists(path)):
       #print "开始运行"
       files = os.listdir(path)
       for each_parent_file_name in files:
           #file1 = file.decode('gbk').encode('utf-8')
           #print "每个文件夹名称:",each_parent_file_name
           if '.bat' not in each_parent_file_name:
               each_parent_file_path = os.path.join(path,each_parent_file_name)
               if(os.path.isdir(each_parent_file_path)):
                   all_seconde_files_name = os.listdir(each_parent_file_path)
                   #print "该文件下含有的二级文件夹数量为：",len(all_seconde_files_name)
                   for each_seconde_file_name in all_seconde_files_name:

                           each_seconde_file_path = os.path.join(each_parent_file_path, each_seconde_file_name)
                           if (os.path.isdir(each_seconde_file_path)):
                               #print "二级路径为：",each_seconde_file_path
                               print "文章数量：",len(os.listdir(each_seconde_file_path))
                               for each_article_name in os.listdir(each_seconde_file_path):
                                   if ".txt"  in  each_article_name:
                                       each_article_path = os.path.join(each_seconde_file_path,each_article_name)
                                       #print each_article_path
                                       info = open(each_article_path,'r')
                                       #print "文章内容：",info.readline()
                                       info.close()

               # h = os.path.split(m)
               # print "dddd", h[1]
               # all_article_list.append(h[1])
       #
       # print list

if __name__ == '__main__':
    file_name = u"毕业论文1325"
    parent_path = r"C:\Users\Administrator\Desktop\2018-05-07"
    path = os.path.join(parent_path, file_name)
    paths = unicode(r"C:\Users\Administrator\Desktop\2018-05-07\毕业论文——语料库 - "
                    r"格式调整 (1325)\毕业论文——语料库 - 格式调整 (1325)", "utf-8")
    print "路径：",paths
    all_article_name = print_path(paths)
    #print '总文件数 =', all_file_num