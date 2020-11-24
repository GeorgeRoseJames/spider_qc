# coding=gbk

from IP import get_ip
import requests
import csv
import re
import time
import traceback
def spider(url,file):
    #这是代理IP
    proxiy = get_ip()
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'guid=811096c87ef5ab49e14234d599c8f567; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lastvisit%3D150400%26%7C%26; partner=www_google_com; 51job=cenglish%3D0%26%7C%26; search=jobarea%7E%60080200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA193%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21',
        'referer':'https://www.51job.com/',
        'Host': 'search.51job.com'
        }
    try:

        req = requests.get(url, headers=headers,proxies=proxiy)
        req.encoding = 'gbk'
        if req.status_code != 200:
            with open('errors.txt','a') as f:
                f.writelines(time.asctime(time.localtime(time.time())))
                f.writelines("响应错误！")
                f.close()
            return None
    except BaseException as error:
        with open('errors.txt', 'a') as f:
            f.writelines(time.asctime(time.localtime(time.time())))
            f.writelines(str(Exception))
            f.writelines(str(error))
            f.writelines(repr(error))
            f.writelines(traceback.print_exc())
            f.writelines('traceback.format_exc():\n%s' % traceback.format_exc())
            f.close()
            return None
    else:
        job_list = []
        pattern = re.compile(r'("job_title":.*?)(?=,"adid")')
        for i in pattern.findall(req.text):
            job_list_base = []
            # print(i)
            # 工作名
            try:

                job_name = re.findall(r'"job_title":"(.*?)",',i)[0].replace('\/','\\')
                job_list_base.append(job_name)

                # 公司名
                job_company = re.findall(r'"company_name":"(.*?)",', i)[0]
                job_list_base.append(job_company)

                # salary
                job_salary = re.findall(r'"providesalary_text":"(.*?)",', i)
                salary = job_salary[0]
                # if salary is lacking , pass it.
                if "" == salary:
                    continue
                # Convert the salary to an annual salary
                # 将\ / 去掉
                salary = salary.replace('\\', '').replace('/', '')
                r = re.compile(r'(\d.*)-(.*\d)')
                if '月' == salary[-1]:
                    m = r.match(salary)
                    if '千' == salary[-2]:
                        salary = str(round(eval(m.group(1)) * 12 / 10)) + '-' + str(round(eval(m.group(2)) * 12 / 10))
                    else:
                        salary = str(round(eval(m.group(1)) * 12)) + '-' + str(round(eval(m.group(2)) * 12))
                elif '年' == salary[-1]:
                    salary = r.match(salary)
                    # Unified format
                    salary = str(salary.group(1)) + '-' + str(salary.group(2))
                else:
                    continue
                job_salary = salary
                job_list_base.append(job_salary)

                # workarea
                job_workarea = re.findall(r'"workarea_text":"(.*?)",',i)[0]
                job_list_base.append(job_workarea)

                # companytype
                job_companytype = re.findall(r'"companytype_text":"(.*?)",', i)[0]
                job_list_base.append(job_companytype)

                # companysize
                job_companysize = re.findall(r'"companysize_text":"(.*?)"',i)[0]
                job_list_base.append(job_companysize)

                # companyind
                job_companyind = re.findall(r'"companyind_text":"(.*?)"',i)[0].replace('\/','\\')
                job_list_base.append(job_companyind)

                # jobwelf
                job_welf_list = re.findall(r'"jobwelf":"(.*?)"',i)[0].split(" ")
                job_list_base.append(job_welf_list)

                # attribute
                job_attribute = re.findall(r'"attribute_text":\[(.*?)]',i)[0].split(",")
                del job_attribute[0]
                del job_attribute[-1]
                if len(job_attribute) == 2:
                   del job_attribute[0]
                if job_attribute:
                    job_attribute = job_attribute[0].replace('\/', '\\')
                else:
                    job_attribute.append("")
                job_list_base.append(job_attribute)

                job_list.append(job_list_base)
                # print(job_name,job_company,job_salary,job_workarea,job_companytype,job_companysize,job_companyind,job_welf_list)
            except BaseException as e:
                with open('errors_append.txt', 'a') as f:
                    f.writelines(time.asctime(time.localtime(time.time())))
                    f.writelines(str(Exception))
                    f.writelines(str(e))
                    f.writelines(repr(e))
                    f.writelines('traceback.format_exc():\n%s' % traceback.format_exc())
                    f.close()
                continue
        # 写入csv文件
        with open(file,'a',newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(job_list)
            f.close()
        time.sleep(0.01)
# spider()