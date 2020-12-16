#coding=gbk
# https://blog.csdn.net/mm_bit/article/details/46988925
# https://blog.csdn.net/zm_1900/article/details/89106643
# https://blog.csdn.net/u011311291/article/details/79731006

import joblib
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba

from sklearn.metrics import accuracy_score,precision_score, \
recall_score,f1_score,cohen_kappa_score

from sklearn.multiclass import OutputCodeClassifier


#导入数据
data_list = []
with open('classify_welfare.txt','r') as f:
    for line in f:
        data_list.append(line.split(" "))
# print(data_list)
welfare_target = []
for data,i in zip(data_list,range(12)):
    welfare_target.extend((np.ones(len(data),int) * i).tolist())
welfare_target = np.array(welfare_target)
# print(len(welfare_target))
# print(welfare_target)
def jieba_tokenize(text):
    return jieba.lcut(text)
tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)

welfare_word = []
for data in data_list:
    welfare_word.extend(data)
welfare_data = tfidf_vectorizer.fit_transform(welfare_word).toarray()

print(welfare_data)
# 划分数据集合
welfare_data_train,welfare_data_test,welfare_target_train,welfare_target_test = \
train_test_split(welfare_data,welfare_target,test_size=0.2,random_state=666)

# 数据标准化
# stdScaler = StandardScaler().fit(welfare_data_train)
# welfare_data_train_std = stdScaler.transform(welfare_data_train)
# welfare_data_test_std = stdScaler.transform(welfare_data_test)

# 建立svm模型，使用线性核函数
model = OutputCodeClassifier(LinearSVC())
model = model.fit(welfare_data_train,welfare_target_train)
# 保存模型
joblib.dump(model, 'welfare_predict.pkl')

welfare_target_predict = model.predict(welfare_data_test)
print('预测前20个结果为：\n',welfare_target_predict[:20])

print('使用SVM预测数据的准确率为：',
      accuracy_score(welfare_target_test,welfare_target_predict))
print('使用SVM预测数据的精确率为：',
      precision_score(welfare_target_test,welfare_target_predict,average='micro'))
print('使用SVM预测数据的召回率为：',
      recall_score(welfare_target_test,welfare_target_predict,average='micro'))
print('使用SVM预测数据的F1值为：',
      f1_score(welfare_target_test,welfare_target_predict,average='micro'))
print('使用SVM预测数据的Cohen’s Kappa系数为：',
      cohen_kappa_score(welfare_target_test,welfare_target_predict))
# 使用SVM预测数据的准确率为： 0.9966957044157405
# 使用SVM预测数据的精确率为： 0.9966957044157405
# 使用SVM预测数据的召回率为： 0.9966957044157405
# 使用SVM预测数据的F1值为： 0.9966957044157405
# 使用SVM预测数据的Cohen’s Kappa系数为： 0.9944571272361682


# #导入数据
# data_list = []
# with open('notes.txt','r', encoding='utf-8') as f:
#     for line in f:
#         data_list.append(line.replace("\n","").split(" "))
# # print(data_list)
# target = [x[0] for x in data_list]
# _data = [x[1:] for x in data_list]
# #print(_data)
# _target = []
# # print(welfare_target)
# for data,i in zip(_data,range(11)):
#     _target.extend((np.array(target[i]).repeat(len(data))).tolist())
# _target = np.array(_target)
# print(_target)
# # print(len(welfare_target))
# # print(welfare_target)
# def jieba_tokenize(text):
#     return jieba.lcut(text)
# tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
#
# _word = []
# for data in _data:
#     _word.extend(data)
# _data = tfidf_vectorizer.fit_transform(_word).toarray()
#
# # print(_data)
# # 划分数据集合
# _data_train, _data_test, _target_train, _target_test = \
# train_test_split(_data, _target, test_size=0.2, random_state=666)
#
# # 数据标准化
# # stdScaler = StandardScaler().fit(welfare_data_train)
# # welfare_data_train_std = stdScaler.transform(welfare_data_train)
# # welfare_data_test_std = stdScaler.transform(welfare_data_test)
#
# # 建立svm模型，使用线性核函数
# model = OutputCodeClassifier(LinearSVC())
# model = model.fit(_data_train, _target_train)
# # 保存模型
# joblib.dump(model, 'work_predict.pkl')
#
# _target_predict = model.predict(_data_test)
# print('预测前20个结果为：\n', _target_predict[:20])
#
# print('使用SVM预测breast_cancer数据的准确率为：',
#       accuracy_score(_target_test, _target_predict))
# print('使用SVM预测breast_cancer数据的精确率为：',
#       precision_score(_target_test, _target_predict, average='micro'))
# print('使用SVM预测breast_cancer数据的召回率为：',
#       recall_score(_target_test, _target_predict, average='micro'))
# print('使用SVM预测breast_cancer数据的F1值为：',
#       f1_score(_target_test, _target_predict, average='micro'))
# print('使用SVM预测breast_cancer数据的Cohen’s Kappa系数为：',
#       cohen_kappa_score(_target_test, _target_predict))
# 性能太差，不采用
#
