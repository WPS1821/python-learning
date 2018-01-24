#_*_ coding:utf-8 _*_
import requests, csv, re
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) QAppleWebkit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
header = ['顺序','书名','评分','作者','出版社','出版时间','评价人数','价格','详情链接']
def get_html(url):
    request = requests.get(url, headers = headers)
    if request.status_code == 200:
        return request.text
    else:
        print('网页无法访问')
        return None
def get_content(num):
    url = 'https://book.douban.com/top250?start=' + str(num * 25)
    response = get_html(url)
    soup = BeautifulSoup(response, 'lxml')
    total = []
    try:
        titles = soup.select('div.pl2 > a')
        name = []
        for i in titles:
            name.append([i['title'], i['href']])
        rating = soup.find_all('span', class_="rating_nums")
        actors = soup.find_all('p', class_="pl")
        comments = soup.find_all('span', class_=re.compile('pl'),limit = 25)
        actor = []
        for i in actors:
            a = i.get_text()
            a = a.split('/')
            k = len(a)
            price = a[k-1]
            publictime = a[k-2]
            public = a[k-3]
            author = "、".join(a[:k-3])
            author = author.replace('・','')
            actor.append([author, public,publictime, price])
            #print(actor)
        peoplenum = []
        for i in comments:
            a = i.get_text().replace('(','')
            a = a.replace('\n','')
            a = a.replace(')','')
            a = a.replace(' ', '')
            a = a[:-2]
            peoplenum.append(a)
        try:
            for i in range(len(titles)):
                total.append([str(num*25+i+1),name[i][0],rating[i].get_text(),actor[i][0],actor[i][1],actor[i][2],peoplenum[i],actor[i][3],name[i][1]])
            # print(len(titles), len(rating), len(actors), len(comments), len(peoplenum))
        except:
            print('获取数据失败')
        return total
    except:
        print('获取详情出错')
        return None
def main():
    with open('douban.csv', 'w', newline ='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        for i in range(10):
            try:
                content = get_content(i)
                if content is not None:
                    print('获取第' + str(i+1) + '页数据成功，正在保存···')
                    try:
                        f_csv.writerows(content)
                        print('保存第' + str(i+1) + '页数据成功')
                    except:
                        print(content)
                        print('保存第' +  str(i+1) + '页数据失败')
            except:
                print('获取第' + str(i+1) + '页数据失败，正在解析下一页')
                pass

if __name__ == "__main__":
    main()