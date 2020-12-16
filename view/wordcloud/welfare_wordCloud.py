#python   3.7.9
# wordcloud   1.8.1
# matplotlib   3.3.2
# PIL   8.0.0
# numpy  1.18.5
# 参考网址  http://f6i.cn/L1E8Hr

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd



pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
total = str()
def welfare_wordCloud(data_locals):
    # list1 = ["北京", "成都", "大连", "广州", "哈尔滨", "杭州", "昆明", "南京", "宁波", "上海", "深圳", "苏州", "武汉", "西安", "长春", "长沙", "重庆"]
    global total
    for local,data in data_locals.items():
        # data = pd.read_csv("data//{}.csv".format(local), encoding="gbk", header=None)
        # data.columns = ["岗位", "公司", "薪资", "位置", "公司性质", "规模", "工作领域", "福利", "学历"]
        # data["福利"] = data["福利"].transform(eval)
        words = []

        def words_add(st):
            words.extend(st)
            return st

        data["福利"].apply(words_add)

        maskph = np.array(Image.open("view\\wordcloud\\地图\\{}地图.jpg".format(local)))
        text_cut = "/".join(words)
        wordcloud = WordCloud(mask=maskph, background_color="white", font_path="msyh.ttc", width=1000, height=860, margin=2,
                          collocations=False).generate(text_cut)
        total = total + text_cut

        plt.imshow(wordcloud)
        plt.axis("off")
        wordcloud.to_file("view\\wordcloud\\福利词云图\\{}福利.png".format(local))

    maskph = np.array(Image.open("view\\wordcloud\\地图\\中国地图.jpg"))
    wordcloud = WordCloud(mask=maskph, background_color="white", font_path="msyh.ttc", width=1000, height=860, margin=2,
                      collocations=False).generate(total)
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file("view\\wordcloud\\福利词云图\\全部福利.png")
