# -*- coding: utf-8 -*-
# @Author: wps18
# @Date:   2018-01-14 13:29:08
# @Last Modified by:   wps18
# @Last Modified time: 2018-01-15 22:23:35
import requests, os, json
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import csv, time, random
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) QAppleWebkit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
header = ['排名','名称','得分','主演','上映时间','国家','类型','详情链接']
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
with open('douban.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    for j in range(14):
        num = j*20
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=' + str(num) + '&limit=20'
        try:
            # pro = random.choice(proxy)
            request = requests.get(url, headers = headers).text #, proxies = pr
            data = json.loads(request)
            print('解析第' + str(j+1) + '页成功')
            imgurl = []
            filename = []
            for i in data:
                # print(i)
                try:
                    imgurl.append(i['cover_url'])
                    # print(imgurl)
                    # print(type(i['rank']))
                    name = str(i['rank']) + str(i['title']) + '.jpg'
                    filename.append(name)
                    print('正在保存第' + str(j + 1) + '页数据···')
                    allinfo = []
                    allinfo.append(i['rank'])
                    allinfo.append(i['title'])
                    allinfo.append(i['score'])
                    a = "、".join(i['actors'])
                    allinfo.append(a)
                    allinfo.append(i['release_date'])
                    region = "".join(i['regions'])
                    allinfo.append(region)
                    type = "、".join(i['types'])
                    allinfo.append(type)
                    allinfo.append(i['url'])
                    print(allinfo)
                    try:
                        f_csv.writerow(allinfo)
                        print('保存文本成功')
                    except:
                        print('保存文本失败')
                except:
                    print('正在保存第' + str(j+1) + '页数据失败···')
                # print(i['rank'])
            for k,j in zip(imgurl, filename):
                print('正在保存图片: ' + k + '---' + j)
                try:
                    urlretrieve(k, j)
                    print('保存图片成功')
                except:
                    print('保存图片失败')
        except:
            print('解析第' + str(j+1) + '页失败')
        time.sleep(2)
print('Done!')
