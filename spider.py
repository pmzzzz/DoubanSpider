import os

from info import Movie
import csv
import requests
from bs4 import BeautifulSoup

# 构造排行榜所有url
def geturls():
    url = 'https://movie.douban.com/top250?start='
    urls = []
    for i in range(0,250,25):
        urls.append(url+str(i))
    return urls

def gethref(url=None):
    headers= {
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        ,"Cookies":'bid=LWfX6h9BFTQ; douban-fav-remind=1; __utmc=30149280; viewed="34836230"; gr_user_id=dbec68e1-05e1-4120-a4bc-2a06acee7277; _vwo_uuid_v2=DDB9B65E6A3EE3AE579BBA5AA810ACBAB|97ffbcba2cd63e895526ecd6b2f93333; ll="108309"; __utmz=30149280.1606440757.9.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1606440760.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=BY8WTHHOwGnr86IgRt5fNRpe6MSUneh0; __gads=ID=f86cc38f1313550c-227899eeafc40058:T=1605255846:S=ALNI_MZhfnFkxtmbrSO2O_JwhNY_lCAzcg; dbcl2="227392355:4FUDWVHGeaQ"; ck=f7yV; push_noty_num=0; push_doumail_num=0; __utmv=30149280.22739; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1606551829%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.169479549.1591099150.1606546204.1606551829.15; __utmb=30149280.0.10.1606551829; __utma=223695111.1746838704.1606440760.1606546204.1606551829.7; __utmb=223695111.0.10.1606551829; _pk_id.100001.4cf6=6003fc09d1c3bb55.1606440760.7.1606553549.1606549100.'
    }
    re = requests.get(url,headers=headers).content
    soup = BeautifulSoup(re,'html.parser')
    olTag = soup.find('ol',{'class':'grid_view'})
    li_all = olTag.find_all('li')
    hrefs = []
    for li in li_all:
        hrefs.append(li.find('a').attrs['href'])
    return hrefs

if __name__ == "__main__":
    # 创建新文件，输入头部信息
    if os.path.exists('豆瓣250.csv'):
        os.remove('豆瓣250.csv')
    with open('豆瓣250.csv','a',encoding='utf-8-sig',newline='') as f:
        writer = csv.writer(f,dialect='excel')
        writer.writerow(['电影名称','导演'])

    for url in geturls():
        for href in gethref(url):
            movie = Movie(url=href)
            movie.getinfo()
            # 追加写入csv
            with open('豆瓣250.csv','a',encoding='utf-8-sig',newline='') as f:
                writer = csv.writer(f,dialect='excel')
                writer.writerow([movie.title,movie.director])
                print('写入成功')

