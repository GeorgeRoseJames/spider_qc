#解析url

from spider import spider
import os
def get_data():
    location = {"杭州":'080200',
                "上海":'020000',
                "北京":'010000',
                "广州":'030200',
                "深圳":'040000',
                '武汉':'180200',
                '宁波':'080300',
                "苏州":'070300',
                '南京':'070200',
                '长沙':'190200',
                '成都':'090200',
                '重庆':'060000',
                '昆明':'250200',
                '西安':'200200',
                '哈尔滨':'220200',
                '大连':'230300',
                '长春':'240200'
                }
    for local,local_code in location.items():
        if not os.path.exists('data'):
            os.mkdir('data')
        file = 'data\\{}.csv'.format(local)
        with open(file,'w') as f:
            f.close()

        for page in range(1,2001):
            url = 'https://search.51job.com/list/{}' \
                  ',000000,0000,00,9,99,+,2,{}.html' \
                  '?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&' \
                  'jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(local_code,page)
            with open('data\\t.text', 'w') as f:
                f.writelines(url)
                f.close()

            spider(url,file)
            print("保存成功！", end=" ")
            print("location:{},page={}".format(local, page))
get_data()
