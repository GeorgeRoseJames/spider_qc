# coding=gbk


import pandas as pd
import sys
import numpy as np
import os
from view.wordcloud.welfare_wordCloud import welfare_wordCloud
from view.wordcloud.work_area_wordCloud import work_area_wordCloud
# from pylab import mpl
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# '''
# 读取数据
# '''
welfare_set = set()
def data_clear(dic_data,locals):
    # 工作领域
    # 福利
    global welfare_set
    os.chdir('..')
    for local in locals:
        try:
            data = pd.read_csv('data\\{}.csv'.format(local), encoding='gbk' ,header=None)
            data.columns = ["岗位","公司","薪资",'位置','公司性质','规模','工作领域','福利','学历']
        except:
            print('error')
            sys.exit()
        else:
            print('{}读取成功！'.format(local))

            # 数据处理


            data["工作领域"] = data["工作领域"].transform(lambda x:list(x.split("\\")))
            # print(len(filed_set))

            # 薪资数据处理
            def func_split_salary(str):
                str = str.split('-')
                str = list(map(float,str))
                str.append(np.mean(str))
                return str
            # print(pd.DataFrame(data['薪资']))
            data['薪资'] = data['薪资'].apply(func_split_salary)
            data = pd.concat([data,data['薪资'].apply(pd.Series,index = ['最低薪资','最高薪资','平均薪资'])],axis=1)
            # data = data.drop(['薪资'],axis=1)
            # 删除大于200的异常数据
            data = data[data['最高薪资'] < 200]
            print(data['最高薪资'].describe())
            # print(np.min(data['最高薪资']))
            # test = data.loc[:,['最高薪资','平均薪资','最低薪资']]
            # test.boxplot()
            # plt.show()


            data['福利'] = data['福利'].transform(eval)
            def func_add_set(list):
                for s in list:
                    welfare_set.add(s)
            data['福利'].apply(func_add_set)

            # 获取
            welfare_set.remove("")
            # print(fuli_set)
            # print(len(fuli_set))
            # out:2703
            #储存数据
            dic_data.update({local:data})


    # 生成词云
    work_area_wordCloud(dic_data)
    welfare_wordCloud(dic_data)
    # 相似性判断
    list_test = list(welfare_set)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    import jieba
    def jieba_tokenize(text):
        return jieba.lcut(text)
    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=False)
    tfidf_matrix = tfidf_vectorizer.fit_transform(list_test)
    # 聚类簇，分为12类
    num_clusters = 12
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=60, init='k-means++', n_jobs=-1)
    result = km_cluster.fit_predict(tfidf_matrix)

    result_list = []
    for i in range(num_clusters):
        result_list.append([])
    # print(len(result))
    for i,j in zip(result,list_test):
        result_list[i].append(j)
    # 存储
    with open('commendation\\classify_welfare.txt','w') as f:
        for i in range(num_clusters):
            f.writelines(list_test[i])
        f.close()

dict_data = dict()
locals = ["杭州","上海","北京","广州","深圳",'武汉','宁波',"苏州",'南京','长沙','成都','重庆','昆明','西安','哈尔滨','长春']
data_clear(dict_data,locals)
