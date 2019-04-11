# encoding: utf-8


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.datasets import load_iris

# 导入IRIS数据集
iris = load_iris()
print type(iris.data)
print iris.data  # 查看数

print "*"*50,"查看数据！！！！！"
print"标签：",iris.target,type(iris.target)
model1 = SelectKBest(chi2, k=50)#选择k个最佳特征
model1.fit_transform(iris.data, iris.target)#iris.data是特征数据，iris.target是标签数据，该函数可以选择出k个特征

print model1.scores_

print model1.pvalues_