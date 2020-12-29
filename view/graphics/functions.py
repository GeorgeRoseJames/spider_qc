import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
import os
os.system("python functions.py")
'''
wt = [[0, '计算机/互联网/通信/电子'], [0, '会计/金融/银行/保险'], [0, '贸易/消费/制造/营运'], [0, '制药/医疗'], [0, '广告/媒体'], [0, '房地产/建筑'],
      [0, '专业服务/教育/培训'], [0, '服务业'], [0, '物流/运输'], [0, '能源/环保/化工'], [0, '政府/非营利组织/其他']]  # 权重wt[i][0]


# 细化分类得到subdivide新的一列
def subdivide(x):
    if x.split('\\')[0] in ['计算机软件', '计算机硬件', '计算机服务(系统、数据服务、维修)', '通信',
                            '互联网', '网络游戏', '电子技术', '仪器仪表']:
        wt[0][0] += 1
        return wt[0][1]
    elif x.split('\\')[0] in ['会计', '金融', '银行', '保险', '信托']:
        wt[1][0] += 1
        return wt[1][1]
    elif x.split('\\')[0] in ['贸易', '批发', '快速消费品(食品、饮料、化妆品) ', '服装', '家具',
                              '奢侈品', '办公用品及设备', '机械', '汽车', '汽车零配件']:
        wt[2][0] += 1
        return wt[2][1]
    elif x.split('\\')[0] in ['制药', '医疗', '医疗设备']:
        wt[3][0] += 1
        return wt[3][1]
    elif x.split('\\')[0] in ['广告', '公关', '影视', '文字媒体', '印刷']:
        wt[4][0] += 1
        return wt[4][1]
    elif x.split('\\')[0] in ['房地产', '建筑', '家居', '物业管理', '中介服务', '租赁服务']:
        wt[5][0] += 1
        return wt[5][1]
    elif x.split('\\')[0] in ['专业服务(咨询、人力资源、财会)', '外包服务', '检测，认证',
                              '法律', '教育', '学术']:
        wt[6][0] += 1
        return wt[6][1]
    elif x.split('\\')[0] in ['餐饮业', '酒店', '娱乐', '美容', '生活服务']:
        wt[7][0] += 1
        return wt[7][1]
    elif x.split('\\')[0] in ['交通', '航天']:
        wt[8][0] += 1
        return wt[8][1]
    elif x.split('\\')[0] in ['石油', '采掘业', '电气', '新能源', '原材料和加工', '环保']:
        wt[9][0] += 1
        return wt[9][1]
    else:
        wt[10][0] += 1
        return wt[10][1]


# 得到对应城市的工作类网络图
# [v['weight'] / 100.0 for (r, c, v) in G.edges(data=True)]不能赋给node_size
# 边的粗细体现权重
def IMPoverview1(loc):
    G = nx.Graph()
    G.add_node(loc)
    plt.figure()
    for i in wt:
        G.add_node(i[1])
        G.add_weighted_edges_from([(loc, i[1], i[0])])
    pos = nx.spring_layout(G, k=20, iterations=20)
    nx.draw(G, pos, node_color=('#7fa7e8'), node_size=2000,
            edge_color=('#7fa7e8'), width=[float(v['weight']) / 600 for (r, c, v) in G.edges(data=True)], with_labels=True, font_size=15, alpha=0.6)
#    plt.savefig('view\\viewer\\networks{}.png'.format(loc))
    plt.savefig('graphics\\networks\\{}.png'.format(loc), bbox_inches='tight')


# 根据薪水取上下限得到low high新的两列
def getLow(x):
    return x.split('-')[0]


def getHigh(x):
    return x.split('-')[1]


dic = {'计算机/互联网/通信/电子': 1, '会计/金融/银行/保险': 2, '贸易/消费/制造/营运': 3, '制药/医疗': 4, '广告/媒体': 5, '房地产/建筑': 6,
       '专业服务/教育/培训': 7, '服务业': 8, '物流/运输': 9, '能源/环保/化工': 10, '政府/非营利组织/其他': 11}


# 同一城市不同类别工资对比
# 最高工资大于40的较少 参考价值不大
# y = row[1]['low']~row[1]['high'] x = dic[row[1]['subdivide']] +- 1
def IMPoverview2(loc):
    x = []
    y = []
    global df
    plt.figure()
    for row in df.iterrows():
        if int(float(row[1]['high'])) > 40:
            continue
        dElta = int(float(row[1]['high'])) - int(float(row[1]['low']))
        x.extend(np.random.uniform(dic[row[1]['subdivide']] - 1, dic[row[1]['subdivide']], size=dElta))
        y.extend(np.random.uniform(int(float(row[1]['low'])), int(float(row[1]['high'])) + 1, size=dElta))
    scale_ls = [i + 0.5 for i in range(11)]
    index_ls = ['计算机/互联网/通信/电子', '会计/金融/银行/保险', '贸易/消费/制造/营运', '制药/医疗', '广告/媒体',
                '房地产/建筑', '专业服务/教育/培训', '服务业', '物流/运输', '能源/环保/化工', '政府/非营利组织/其他']
    plt.xticks(scale_ls, index_ls, rotation=60)  # 可以设置坐标字
    '''
    # Hide major tick labels
    plt.set_xticklabels('')
    # Customize minor tick labels
    plt.set_xticks(scale_ls, minor=True)
    plt.set_xticklabels(index_ls, minor=True)
    '''
    plt.scatter(x, y, c='#7fa7e8', alpha=0.002)
    plt.xlabel("工作类")
    plt.ylabel("万元")
    plt.title('最高工资不高于40W元不同工作类的薪资分布对比')
#    plt.savefig('view\\viewer\\histogram{}.png'.format(loc))
    plt.savefig('graphics\\histogram\\{}.png'.format(loc), bbox_inches='tight')


# IMPoverview1()
def main(locals):
    # 防止添加中文标签和标题时出现乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 读入数据到df
    # NOTC = nature of the company
    # 自动补全缺失数据为NaN
    global df
    for local in locals:
        df = pd.read_csv('{}.csv'.format(local), names=['job', 'company', 'salary', 'location', 'NOTC', 'needing', 'lable', 'welfare', 'requirement'],
                         keep_default_na=False, encoding='gbk')
        df['subdivide'] = df['lable'].apply(subdivide)
        df['low'] = df['salary'].apply(getLow)
        df['high'] = df['salary'].apply(getHigh)
        IMPoverview1(local)
        IMPoverview2(local)

'''
ll = ["杭州", "上海", "北京", "广州", "深圳", '武汉', '宁波', "苏州",
          '南京', '长沙', '成都', '重庆', '昆明', '西安', '哈尔滨', '长春']
main(ll)
'''