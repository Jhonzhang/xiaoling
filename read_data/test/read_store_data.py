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
def print_path(path):
   list= []
   print "调用该程序"
   if(os.path.exists(path)):
       print "开始运行"
       files = os.listdir(path)
       for file in files:
           file = file.decode('gbk').encode('utf-8')
           print file
       #     m = os.path.join(path,file)
       #     if(os.path.isdir(m)):
       #         h = os.path.split(m)
       #         print h[1]
       #         list.append(h[1])
       #
       # print list

if __name__ == '__main__':
    print_path(r'C:\Users\Administrator\Desktop\biyelunwen1325')
    #print '总文件数 =', all_file_num