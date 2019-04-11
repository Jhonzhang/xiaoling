
# coding: utf8
#from __future__ import division
import os


def CHI_control_text(text, ca_num, textname, categoryName):
    # 针对每个文章中只保留根据CHI值选取的特征词，使一会儿构成的特征词仅仅由这些组成
    CHI_order_select = open("CHIorder" + '\\' + 'class' + str(ca_num) + "_CHIorder_select.txt", 'r')
    if not os.path.exists("text_remain\\sougou_all" + '\\' + categoryName):
        os.makedirs("text_remain\\sougou_all" + '\\' + categoryName)
    text_remain = open("text_remain" + '\\' + textname, 'w')
    # 根据CHI筛选后的词语对给每个文章的分词结果进行修改，也就是只保留每篇文章中出现这些词的

    dict = {}
    for kv in [d.strip() for d in CHI_order_select]:
        dict[kv] = kv  # 读入对应类别的保留词
    have_word_num = 0  # 用来记录本篇文章中共有几个关键词
    for line in text.readlines():
        # print line.strip()
        text_info = line.strip().split('\t')
        if dict.has_key(text_info[0].strip()):
            have_word_num += 1
            # 判断本篇文章中的词是否是保留词，如是，写入这篇文章的text_remain中
            text_remain.write(text_info[0].strip() + '\n')

    if have_word_num < 2:  # 把出现关键词个数少于2的文章的文章删除，这种文章几乎和本主题没有什么关系
        text_remain.close()
        os.remove("text_remain" + '\\' + textname)
    else:
        text_remain.close()


# 得到每个类别下，文章的数目
class1_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "aoyun"))
class2_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "fangchan"))
class3_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "jiankang"))
class4_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "jiaoyu"))
class5_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "lvyou"))
class6_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "qiche"))
class7_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "shangye"))
class8_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "shishang"))
class9_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "tiyu"))
class10_num = len(os.listdir("wordtimes\\sougou_all" + '\\' + "yule"))

# 得到每个类别下，每个词在多少个文章中出现
dict_1 = {}
with open("wordtimes\\sougou_all" + '\\' + "aoyun_classtimes.txt", 'r') as df1:
    for kv in [d.strip().split('\t') for d in df1]:
        dict_1[kv[0].decode('utf-8')] = kv[1]
# for k in dict_gaokao:  #这个k是只有单词的
#     print k,dict_gaokao[k]
dict_2 = {}
with open("wordtimes\\sougou_all" + '\\' + "fangchan_classtimes.txt", 'r') as df2:
    for kv in [d.strip().split('\t') for d in df2]:
        # print kv[0].decode('utf-8')
        dict_2[kv[0].decode('utf-8')] = kv[1]

dict_3 = {}
with open("wordtimes\\sougou_all" + '\\' + "jiankang_classtimes.txt", 'r') as df3:
    for kv in [d.strip().split('\t') for d in df3]:
        dict_3[kv[0].decode('utf-8')] = kv[1]

dict_4 = {}
with open("wordtimes\\sougou_all" + '\\' + "jiaoyu_classtimes.txt", 'r') as df4:
    for kv in [d.strip().split('\t') for d in df4]:
        dict_4[kv[0].decode('utf-8')] = kv[1]

dict_5 = {}
with open("wordtimes\\sougou_all" + '\\' + "lvyou_classtimes.txt", 'r') as df5:
    for kv in [d.strip().split('\t') for d in df5]:
        dict_5[kv[0].decode('utf-8')] = kv[1]

dict_6 = {}
with open("wordtimes\\sougou_all" + '\\' + "qiche_classtimes.txt", 'r') as df6:
    for kv in [d.strip().split('\t') for d in df6]:
        dict_6[kv[0].decode('utf-8')] = kv[1]

dict_7 = {}
with open("wordtimes\\sougou_all" + '\\' + "shangye_classtimes.txt", 'r') as df7:
    for kv in [d.strip().split('\t') for d in df7]:
        dict_7[kv[0].decode('utf-8')] = kv[1]

dict_8 = {}
with open("wordtimes\\sougou_all" + '\\' + "shishang_classtimes.txt", 'r') as df8:
    for kv in [d.strip().split('\t') for d in df8]:
        dict_8[kv[0].decode('utf-8')] = kv[1]

dict_9 = {}
with open("wordtimes\\sougou_all" + '\\' + "tiyu_classtimes.txt", 'r') as df9:
    for kv in [d.strip().split('\t') for d in df9]:
        dict_9[kv[0].decode('utf-8')] = kv[1]

dict_10 = {}
with open("wordtimes\\sougou_all" + '\\' + "yule_classtimes.txt", 'r') as df10:
    for kv in [d.strip().split('\t') for d in df10]:
        dict_10[kv[0].decode('utf-8')] = kv[1]

for class_num in range(1, 11):  # 这里注意才是1到10  用于遍历每个class词典
    dictname = locals()['dict_' + str(class_num)]  # 超级棒的一个locals()[]，可以这样得到变量的名字
    CHI_dic = {}  # 用于记录这个class中每个词的卡方检验值
    for kv in dictname:  # 遍历这个类别下的每个词，把这个类别下每个词的CHI值比较一下，取前100个
        # print kv  #记录这个单词名称
        kv_out_class = 0  # 统计一个新词时，初始化本类别外用到这个词的文档数目为0  相当于b
        not_kv_out_class = 0  # 统计一个新词时，初始化本类别外没有用到这个词的文档数目为0  相当于d
        kv_in_class = int(dictname[kv])  # 记录在这个分类下包含这个词的文档的数量  相当于a
        # print type(kv_in_class)  #注意这里得到的是str型的，一会儿做减法要类型转换
        not_kv_in_class = (locals()['class' + str(class_num) + '_num']) - kv_in_class  ##记录在这个分类下不包含这个词的文档的数量  相当于c
        for class_compare in range(1, 11):
            if class_compare != class_num:
                comparename = locals()['dict_' + str(class_compare)]
                if comparename.has_key(kv):
                    kv_out_class += int(comparename[kv])
                    not_kv_out_class += (locals()['class' + str(class_compare) + '_num']) - kv_in_class

        CHI_dic[kv] = ((kv_in_class * not_kv_out_class - kv_out_class * not_kv_in_class) ** 2) / (
                    (kv_in_class + kv_out_class) * (not_kv_in_class + not_kv_out_class))
        # print kv,CHI_dic[kv]
    # print sys.getdefaultencoding()
    CHI_order = open("CHIorder" + '\\' + 'class' + str(class_num) + "_CHIorder.txt", 'w')
    CHI_order.write(('\n'.join(sorted(CHI_dic, key=CHI_dic.get, reverse=True))).encode('utf-8'))

    fin = open("CHIorder" + '\\' + 'class' + str(class_num) + "_CHIorder.txt", 'r')
    N = int(0.015 * len(locals()['dict_' + str(class_num)]))  # 只取CHI值较大的前0.015个单词
    print ("从第%d类中选出%d个关键词" % (class_num, N))
    CHI_order_select = open("CHIorder" + '\\' + 'class' + str(class_num) + "_CHIorder_select.txt", 'w')
    for line in fin.readlines()[0:N]:  # 得到CHI值较大的N个单词作为当前的特征词，N和本类别的单词的数量有关
        CHI_order_select.write(line.strip() + '\n')

# 下面得到每个文章中出现这些被选出词的情况，也就是使一会儿构成的特征词仅仅由这些组成
rootpath = "..\seg and anno" + "\\" + "results" + "\\" + "sougou_all"
category = os.listdir(rootpath)
ca_num = 1
for categoryName in category:  # 循环类别文件，OSX系统默认第一个是系统文件
    # if categoryName == 'yule':
    if (categoryName == '.DS_Store'): continue
    categoryPath = os.path.join(rootpath, categoryName)  # 这个类别的路径
    filesList = os.listdir(categoryPath)  # 这个类别内所有文件列表
    for filename in filesList:
        if (filename == '.DS_Store'): continue
        textname = (os.path.join(categoryPath, filename))[24:]  # gaokao\1.txt
        contents = open(os.path.join(categoryPath, filename))
        text_remain = CHI_control_text(contents, ca_num, textname, categoryName)
        # break
    ca_num += 1
    # break

print ("CHI_run is finished!")
