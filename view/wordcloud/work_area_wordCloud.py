from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
total=str()

# locals=["北京", "成都", "大连", "广州", "哈尔滨", "杭州", "昆明", "南京", "宁波", "上海", "深圳", "苏州", "武汉", "西安", "长春", "长沙", "重庆"]
def work_area_wordCloud(data_locals):
    global total
    for local,data in data_locals.items():
        # data = pd.read_csv("data//{}.csv".format(local),encoding="gbk",header=None)
        # data.columns =["岗位","公司","薪资","位置","公司性质","规模","工作领域","福利","学历"]
        # data["工作领域"] = data["工作领域"].transform(lambda x:list(x.split("\\")))
        words = []

        def words_add(st):
            words.extend(st)
            return st
        data["工作领域"].apply(words_add)
    
        maskph = np.array(Image.open("view\\wordcloud\\地图\\{}地图.jpg".format(local)))
        text_cut  =  "/".join(words)
        wordcloud = WordCloud(mask =maskph,  background_color="white",font_path = "msyh.ttc", width=1000, height=860, margin=2,collocations=False).generate(text_cut)
        total=total+text_cut

        plt.imshow(wordcloud)
        plt.axis("off")
        wordcloud.to_file("view\\wordcloud\\工作领域词云图\\{}.png".format(local))

    
    maskph = np.array(Image.open("view\\wordcloud\\地图\\中国地图.jpg"))
    wordcloud = WordCloud(mask =maskph,  background_color="white",font_path = "msyh.ttc", width=1000, height=860, margin=2,collocations=False).generate(total)
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file("view\\wordcloud\\工作领域词云图\\中国地区.png")
#wordcloud版本为1.8.1
#matplotlib版本为3.3.2
#PIL版本为8.0.0
#numpy版本为1.18.5
#参考CSDN技术社区有关python词云博客 https://blog.csdn.net/qq_34908107/article/details/80526182

