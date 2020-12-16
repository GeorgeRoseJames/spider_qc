"""
函数作用：用于爬取ip网站生成IP，对后续爬取提供ip
"""
from bs4 import BeautifulSoup
import requests
import random
import re

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    for i in range(0, len(ip_list)):
        ip_info = ip_list[i]
        tag1 = re.compile('\n\t\t\t')
        tag2 = re.compile('\t\t')
        ip_list[i] = tag1.sub('', ip_list[i])
        ip_list[i] = tag2.sub('', ip_list[i])
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_ip():
    url = 'https://www.89ip.cn/'
    headers = {
        # 此处User-Agent替换为自己的
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    return proxies
# print(get_ip())
