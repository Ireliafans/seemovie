#!coding=utf-8
import argparse
import sys
import random
import re
import requests
import lxml.html
import urllib.request
import datetime
import threading
from lxml import etree
from queue import Queue
from bs4 import BeautifulSoup 
from lxml import etree
from urllib import request
from urllib import parse
from multiprocessing import Pool

G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

def banner():#界面
    print("""%s
███████╗███████╗███████╗███╗   ███╗ ██████╗ ██╗   ██╗██╗███████╗
██╔════╝██╔════╝██╔════╝████╗ ████║██╔═══██╗██║   ██║██║██╔════╝
███████╗█████╗  █████╗  ██╔████╔██║██║   ██║██║   ██║██║█████╗  
╚════██║██╔══╝  ██╔══╝  ██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██║██╔══╝  
███████║███████╗███████╗██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██║███████╗
╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝ 
%s        
OPTIONS:                   EXAMPLE:
 -f, Find a movie           python seemovie.py -f 黑豹 
 -n, Search new movie       python seemovie.py -n 
 -s, Search hot movie       python seemovie.py -s

%s # Made By Imanfeng """ % (B,W,B))


def parse_args():#命令
    parser = argparse.ArgumentParser(description='HAVE FUN')
    parser.error = parse_error
    parser._optionals.title='OPTIONS'
    parser.add_argument('-f', '--name', default='',help="Find a movie")
    parser.add_argument('-n', '--new', action='store_const', const='1', help="Search new movie")
    parser.add_argument('-s', '--hot', action='store_const', const='1', help="Search hot movie")
    return parser.parse_args()


def parse_error(errormsg):#错误
    print(("%s[Error] " + errormsg) % (R))
    sys.exit()


# ----------------------------------------------------------------------------------------------------------------------
class find_a_movie:
    """docstring for find_a_movie"""
    def __init__(self, name):#定义
        now = datetime.datetime.now()
        start = (now.hour*60*60)+(now.minute*60)+(now.second)
        self.finalall = {}
        self.web1_keyword = parse.quote(name.encode("gbk"))
        self.web23_keyword = parse.quote(name)
        self.moviewebs()
        self.search()
        pool = Pool()       
        pool.map(self.ygdy8_search ,self.result1_urls)
        pool.map(self.btbtdy_search ,self.result2_urls)
        pool.map(self.btwhat_search ,self.result3_urls)
        dnow = datetime.datetime.now()
        down = (dnow.hour*60*60)+(dnow.minute*60)+(dnow.second)
        time = down - start
        print(("\n%sDONE: USE %d sec")%(W,time))
        

    def moviewebs(self):#网址
        web1_baseurl = "http://www.ygdy8.com"#阳关电影
        web2_baseurl = "http://www.btbtdy.com/"#BT电影天堂
        web3_baseurl = "http://www.btwhat.info"#Btbook

        web1_findurl = "http://s.ygdy8.com/plus/so.php?kwtype=0&keyword="#阳关电影搜索页
        web2_findurl = "http://www.btbtdy.com/search/"#BT电影天堂搜索
        web3_findurl = "http://www.btwhat.info/search/b-"#Btbook搜索页
        self.baselist = [web1_baseurl,web2_baseurl,web3_baseurl]
        self.findlist = [web1_findurl,web2_findurl,web3_findurl]
    

    def get_headers(self):#隐藏UA
        user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
        ]
        ua = random.choice(user_agent_list)
        self.headers = {'User-Agent': ua}
        return self.headers


    def search(self):#搜索电影
        print(("%sSearch...") % (G))
        self.baseurl = []
        self.baseurl.append(self.findlist[0]+self.web1_keyword)
        self.baseurl.append(self.findlist[1]+self.web23_keyword+".html")
        self.baseurl.append(self.findlist[2]+self.web23_keyword+".html")
        xpaths = ['//div[@class="co_content8"]/ul//a','//div[@class="list_so"]//dd[@class="lf"]/p/strong/a','//div[@class="search-item"]/div[1]/h3//a']
        self.result1_urls = []#阳关电影搜索结果
        self.result2_urls = []#BT电影天堂搜索结果
        self.result3_urls = []#Btbook搜索结果
        for i in range(3):
                try:
                    res = requests.get(self.baseurl[i], headers={'User-Agent':str(self.get_headers())} ,timeout=3)
                    res.encoding = res.apparent_encoding
                    html = etree.HTML(res.text)
                    tags = html.xpath(xpaths[i])
                    for tag in tags:
                        url = self.baselist[i] + tag.get('href')
                        if i==0:
                            self.result1_urls.append(url)
                        elif i==1:
                            self.result2_urls.append(url)
                        elif i==2:
                            self.result3_urls.append(url)
                except Exception:
                    break


    def ygdy8_search(self, url):#阳关电影搜索
        refer = self.baseurl[2]+'&searchtype=title'
        try:
            res = requests.get(url, headers={'User-Agent':str(self.get_headers()), 'referer':refer})
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.text)
            title = html.xpath('//div[@class="bd3r"]//div[@class="title_all"]/h1/font')[0].text
            downloads = html.xpath('//div[@id="Zoom"]//table//a/@href')
            print(('%s[%s]') % (W,title))
            for download in downloads:
                print(('[%s迅雷下载%s] [%s%s%s]') % (B,W,B,download,W))
                print('\n|----------------------------------------------------------|\n')
        except Exception:
            pass


    def btbtdy_search(self, url):#BT电影天堂搜索
        refer = self.baseurl[0]+'&searchtype=title'
        try:
            response = urllib.request.urlopen(url)
            html = str(response.read(),'utf-8')
            title = re.findall(r"charset=\"UTF-8\"><title>(.*?)</title>",html)
            print(('%s[%s]') % (W,title[0]))
            print(('[%s搜索链接%s] [%s%s%s]') % (B,W,B,url,W))
            print('\n|----------------------------------------------------------|\n')
        except Exception:
            pass


    def btwhat_search(self, url):#Btbook搜索
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = { 'User-Agent' : user_agent}
        try:
            req = urllib.request.Request(url, headers=header)
            req.add_header('Referer', str(self.baseurl[2]))
            response = urllib.request.urlopen(req)
            html = response.read()
            download = re.findall(r"div class=\"panel-body\">\\n<a href=\"(.*?)\">",str(html))
            titles = re.findall(r"target=\"_blank\" class=\"pill\">(.*?)</a>",str(html.decode('utf-8')))
            str1 = ''
            for title in titles:
                str1 = str1 + title
                str1 = str1 + ' '
            print(('%s[%s]') % (W,str1))
            print(('[%s迅雷下载%s] [%s%s%s]') % (B,W,B,download[0],W))
            print('\n|----------------------------------------------------------|\n')
        except Exception:
            pass


# ----------------------------------------------------------------------------------------------------------------------
class search_movie:
    """docstring for searchnew"""
    def __init__(self, findurl, referurl):#
        self.findurl = findurl
        self.referurl = referurl
        now = datetime.datetime.now()
        start = (now.hour*60*60)+(now.minute*60)+(now.second)
        self.search_url()
        pool = Pool()       
        pool.map(self.search_movie ,self.result1_urls)
        dnow = datetime.datetime.now()
        down = (dnow.hour*60*60)+(dnow.minute*60)+(dnow.second)
        time = down - start
        print(("\n%sDONE: USE %d sec")%(W,time))


    def search_url(self):
        try:
            self.result1_urls = []
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            res = requests.get(self.findurl, headers={'User-Agent':user_agent, 'referer':str(self.referurl)})
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.text)
            # title = html.xpath('//*[@id="header"]//div[@class="bd2"]//div[@class="bd3"]//div[@class="bd3l"]//div[@class="co_area2"]//div[@class="co_content2"]/ul/a')[0].text
            downloads = html.xpath('//*[@id="header"]//div[@class="bd2"]//div[@class="bd3"]//div[@class="bd3l"]//div[@class="co_area2"]//div[@class="co_content2"]/ul/a/@href')
            for download in downloads:
                self.result1_urls.append('http://www.ygdy8.com'+download)
        except Exception:
            pass


    def search_movie(self, url):
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            res = requests.get(url, headers={'User-Agent':user_agent, 'referer':str(self.referurl)})
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.text)
            title = html.xpath('//*[@id="header"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/h1/font')[0].text
            downloads = html.xpath('//div[@id="Zoom"]//table//a/@href')
            print(('%s[%s]') % (W,title))
            print(('[%s迅雷下载%s] [%s%s%s]') % (B,W,B,downloads[0],W))
            print('\n|----------------------------------------------------------|\n')
        except Exception:
            pass


# ----------------------------------------------------------------------------------------------------------------------

def main(moviename, isnewmovie, ishotmovie):
    hot_web1_baseurl = "http://www.ygdy8.com/html/gndy/index.html"#阳关电影高分电影
    new_web1_baseurl = "http://www.ygdy8.com/"#阳关电影最新发布170部
    if moviename!='':
        find_a_movie(moviename)
    elif ishotmovie=='1':
        search_movie(hot_web1_baseurl, new_web1_baseurl)
    elif isnewmovie=='1':
        search_movie(new_web1_baseurl, hot_web1_baseurl)


if __name__ == '__main__':
    banner()
    args = parse_args()
    moviename = args.name
    isnewmovie = args.new
    ishotmovie = args.hot
    main(moviename, isnewmovie, ishotmovie)