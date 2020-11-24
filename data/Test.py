#coding=gbk
import pandas as pd

p = pd.read_csv('上海.csv',encoding='gbk')
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
print(pd.DataFrame(p).head(5))