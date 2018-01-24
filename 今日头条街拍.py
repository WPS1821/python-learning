# -*- coding: utf-8 -*-
# @Author: wps18
# @Date:   2018-01-14 13:29:08
# @Last Modified by:   wps18
# @Last Modified time: 2018-01-16 13:14:37
import requests, os, json, re
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import csv, time, random
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) QAppleWebkit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
# def get_proxy():
#     os.chdir(r'F:\\桌面\\Documents\\wps1\\色影无忌')
#     # headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nex
#     # us 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
#     fp = open('proxy1.txt', 'r')
#     ips = fp.readlines()
#     proxys = list()
#     for p in ips:
#         ip = p.strip('\n').split('\t')
#         proxy = 'http://' + ip[0] + ':' + ip[1]
#         proxies = {'proxy': proxy}
#         proxys.append(proxies)
#     fp.close()
#     return proxys
# proxy = get_proxy()

def get_html(num):
    url = 'https://www.toutiao.com/search_content/?offset=' + str(
        num*20) + '&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab'
    try:
        # pro = random.choice(proxy)
        request = requests.get(url, headers = headers) #, proxies = pr
        if request.status_code == 200:
            datas = json.loads(request.text)
            print('解析第' + str(num+1) + '页成功')
            img = []
            name= []
            for i in datas['data']:
                try:
                    url_1 = 'https://www.toutiao.com/a' + str(i['id']) + '/'
                    # print(url_1)
                    img.append(url_1)
                    name.append(i['title'])
                    # print(i['title'])
                except:
                    print('获取图片信息失败')
            return img, name
        else:
            print('解析第' + str(j + 1) + '页失败')
    except:
        print('访问第' + str(j + 1) + '页失败')

def get_detail(num):
    img, name = get_html(num)
    for i,k in zip(img, name):
        # print(i,k)
        try:
            response = requests.get(i, headers=headers)
            # print(response.status_code)
            if response.status_code == 200:
                pattern = re.compile('quot;(http://p.*?/large/.*?)&quot', re.S)
                # patt_title = re.compile('media_id.*?"name":"(.*?)","user', re.S)
                # title = re.findall(patt_title, response.text)
                # t = "".join(title)
                con = re.findall(pattern, response.text)
                a = 0
                for j in con:
                    # print(j)
                    a = a + 1
                    try:
                        urlretrieve(j, getDownloadPath(a,k))
                        print('保存图片-- '+ str(a) + '- '  + j +  ' --成功')
                    except:
                        print('保存图片失败')
        except:
            print('wrong')
    pass

def getDownloadPath(num, name):
    path = "F:\\桌面\\Documents\\wps1\\今日头条\\" + str(name)
    # directory = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)
        print('创建目录成功')
    path = path + "\\" + str(num) + '.jpg'
    return path
for i in range(7):
    get_detail(i)
    time.sleep(2)
print('Done!')
