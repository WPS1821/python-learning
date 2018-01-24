import requests
from bs4 import BeautifulSoup
import os
import urllib
import random
import time


class mzitu():

    def get_proxy(self):
        os.chdir(r'F:\\桌面\\Documents\\wps1\\色影无忌')
        # headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nex
        # us 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
        fp = open('proxy1.txt', 'r')
        ips = fp.readlines()
        proxys = list()
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'http://' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
        fp.close()
        return proxys

    def all_url(self, url):
        try:
            html = self.request(url)
            all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
            try:
                for a in all_a:
                    try:
                        title = a.get_text()
                        print(u'开始保存：', title)
                        path = str(title).replace("?", '_')
                        if not self.mkdir(path): ##跳过已存在的文件夹
                            print(u'已经跳过：', title)
                            continue
                        href = a['href']
                        # print(href)
                        self.html(href)
                    except:
                        pass
            except:
                print('wrong1')
        except:
            print('wrong2')
    def html(self, href):
        try:
            html = self.request(href)
            max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
            try:
                for page in range(1, int(max_span) + 1):
                    page_url = href + '/' + str(page)
                    self.img(page_url)
            except:
                print('wrong3')
        except:
            print('wrong4')
            return None

    def img(self, page_url):
        # time.sleep(2)
        try:
            img_html = self.request(page_url)
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
            print(img_url)
            self.save(img_url,page_url)
        except:
            print('wrong5')
            return None


    def save(self, img_url, page_url):
        name = img_url[-9:-4]
        try:
            img = self.requestpic(img_url,page_url)
            f = open(name + '.jpg', 'ab')
            f.write(img.content)
            f.close()
        except FileNotFoundError: ##捕获异常，继续往下走
            print(u'图片不存在已跳过：', img_url)
            return False

    def mkdir(self, path): ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("F:\桌面\Documents\wps1\妹子图", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("F:\桌面\Documents\wps1\妹子图", path))
            os.chdir(os.path.join("F:\桌面\Documents\wps1\妹子图", path)) ##切换到目录
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def requestpic(self, url, Referer): ##这个函数获取网页的response 然后返回
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        try:
            ua = random.choice(user_agent_list)
            headers = {'User-Agent': ua,"Referer":Referer} ##较之前版本获取图片关键参数在这里
            content = requests.get(url, headers=headers)
            return content
        except:
            print('wrong3')
            return None

    def request(self, url): ##这个函数获取网页的response 然后返回
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
            content = requests.get(url, headers=headers,proxies = random.choice(Mzitu.proxy),timeout = 10)
            return content
        except:
            print('wrong6')
            return None


Mzitu = mzitu() ##实例化
Mzitu.proxy = Mzitu.get_proxy()
Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
print(u'恭喜您下载完成啦！')
