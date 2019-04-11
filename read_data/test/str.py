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

# str = "张 腾飞 洛阳 中国 中山大学"
# print str.split(' ')
list_1 = ['ztf','张腾飞','宋依']
list_2 = ['河南','洛阳','广州']
list_3 = ['湖南sss','hhhhh益阳','成都']
list_happy = []

list_happy.extend(list_1)

print list_happy
list_happy.extend(list_2)
print list_happy
# list_happy.append(list_3)
# print list_happy