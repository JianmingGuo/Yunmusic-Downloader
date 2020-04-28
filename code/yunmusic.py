import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import json
import time

#功能一：下载单一歌曲、歌词

def single_song(song_id,path,song_name):                    #下载单一歌曲，输入为歌曲id，保存路径，歌曲名称
    song_url = "http://music.163.com/song/media/outer/url?id=%s" % song_id
    down_path = path +'\\'+ song_name + '.mp3'
    urlretrieve(song_url,down_path)
    print("歌曲下载完成："+song_name)

def save2txt(songname, lyric,path):         #写进歌词到指定路径，并保存，输入为歌曲名称、歌词信息、保存路径
    # print('正在保存歌曲：{}'.format(songname))
    print("歌词下载完成："+songname)
    lyric_path=path+'\\'+songname+'.txt'
    with open(lyric_path, 'a', encoding='utf-8')as f:
        f.write(lyric)

def single_song_lyric(song_id,path,song_name):              #下载单一歌曲的歌词，输入为歌曲id，保存路径，歌曲名称
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    json_obj = json.loads(html)
    initial_lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lyric = re.sub(reg, '', initial_lyric).strip()
    save2txt(song_name, lyric, path)
    time.sleep(1)


#功能二：根据歌单url下载

def songs_from_list(url,path):            #url:歌单网址；path:本地保存目录  下载某一歌单的所有歌曲（包括歌手页、排行榜）
    new_url = url.replace('/#', '')

    header = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }

    res = requests.get(new_url, headers=header).text

    r = BeautifulSoup(res, "html.parser")
    music_dict = {}
    result = r.find('ul', {'class', 'f-hide'}).find_all('a')
    for music in result:
        print(music)
        music_id = music.get('href').strip('/song?id=')
        music_name = music.text
        music_dict[music_id] = music_name
    for song_id in music_dict:
        song_url = "http://music.163.com/song/media/outer/url?id=%s" % song_id
        down_path=path+'\\'+music_dict[song_id]+'.mp3'

        # path = "C:\\Users\\ming-\\Downloads\\%s.mp3" % music_dict[song_id]

        # 添加数据
        print( "正在下载：%s" % music_dict[song_id])
        # text.see(END)
        # text.update()

        urlretrieve(song_url, down_path)

def get_lyrics(songids):        #根据歌曲id获取歌词，输入为歌曲Id
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(songids)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    json_obj = json.loads(html)
    initial_lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lyric = re.sub(reg, '', initial_lyric).strip()
    return lyric

def lyrics_from_list(url,path):                 #根据歌单下载歌曲歌词
    new_url = url.replace('/#', '')

    header = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }

    res = requests.get(new_url, headers=header).text

    r = BeautifulSoup(res, "html.parser")
    music_dict = {}
    result = r.find('ul', {'class', 'f-hide'}).find_all('a')
    for music in result:
        print(music)
        music_id = music.get('href').strip('/song?id=')
        music_name = music.text
        music_dict[music_id] = music_name
    songids=music_dict.keys()
    for i in songids:
        lyric=get_lyrics(i)
        save2txt(music_dict[i],lyric,path)
        time.sleep(1)


#功能三：根据歌手下载

#获取歌手信息和id
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re
# chrome_driver = "D:\\software\\chromedriver_win32\\chromedriver.exe"  #chromedriver的文件位置
# browser = webdriver.Chrome(executable_path = chrome_driver)
# wait = WebDriverWait(browser, 5)  # 设置等待时间
def get_singer(url):    # 返回歌手名字和歌手id,输入为歌手详情页
    chrome_driver = "D:\\software\\chromedriver_win32\\chromedriver.exe"  # chromedriver的文件位置
    browser = webdriver.Chrome(executable_path=chrome_driver)
    wait = WebDriverWait(browser, 5)  # 设置等待时间
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.nm.nm-icn.f-thide.s-fc0')
    singername = []
    singerid = []
    for snames in info:
        name = snames.get_text()
        songid = str(re.findall('href="(.*?)"', str(snames))).split('=')[1].split('\'')[0]   #正则表达式获取歌曲id
        singername.append(name)
        singerid.append(songid)
    return zip(singername, singerid)

def get_data(url):
    data = []
    for singernames, singerids in get_singer(url):
        info = {}
        info['歌手名字'] = singernames
        info['歌手ID'] = singerids
        data.append(info)
    return data

def save2csv(url):
    print('保存歌手信息中...请稍后查看')
    with open('singer.csv', 'a', newline='', encoding='utf-8-sig') as f:
        # CSV 基本写入用 w，追加改模式 w 为 a
        fieldnames = ['歌手名字', '歌手ID']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = get_data(url)
        print(data)
        writer.writerows(data)
        print('保存成功')

def download_singer():
    idlist = [1001, 1002, 1003, 2001, 2002, 2003, 4001, 4002, 4003, 6001, 6002, 6003, 7001, 7002, 7003]
    for id in idlist:
        url = 'https://music.163.com/#/discover/artist/cat?id={}&initial=-1'.format(id)
        save2csv(url)

def get_id(singer_name):                    #根据歌手姓名获取对应的歌手id，输入为歌手姓名
    file = "lib\\singer_info.csv"
    with open(file, 'r',encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        name = []
        id = []
        for i in reader:
            name.append(i[0])
            id.append(i[1])
    a=name.index(singer_name)
    return id[a]


#根据歌手姓名下载
def get_html(url):                  #通过代理获取网页信息，输入为指定网页url
    proxy_addr = {'http': '61.135.217.7:80'}
    # 用的代理 ip，如果被封或者失效，在http://www.xicidaili.com/换一个
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, proxies=proxy_addr).text
        return html
    except BaseException:
        print('request error')
        pass

def get_top50(html):                #获取热度前50名的歌曲，并返回对应的歌曲名称和歌曲id，输入为歌手详情页
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.f-hide #song-list-pre-cache a')
    songname = []
    songids = []
    for sn in info:
        songnames = sn.getText()
        songname.append(songnames)
    for si in info:
        songid = str(re.findall('href="(.*?)"', str(si))).strip().split('=')[-1].split('\'')[0]    # 用re查找，查找对象一定要是str类型
        songids.append(songid)
    return zip(songname, songids)

def lyrics_from_singername(name,path):          #根据歌手姓名下载热度前50名歌曲的歌词
    id=get_id(name)
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        lyric = get_lyrics(singer_info[1])
        save2txt(singer_info[0], lyric, path)
        time.sleep(1)

def save_song(songurl, path,songname):              #下载指定链接的歌曲，并保存到指定路径，输入为歌曲下载链接、保存路径、歌曲名称
    try:
        urlretrieve(songurl, path)
        print('歌曲下载完成：' + songname)
    except BaseException:
        print('下载失败：' + songname)
        pass

def songs_from_singername(name,path):                    #根据歌手姓名下载歌曲到指定路径，输入为歌手姓名和保存路径
    id=get_id(name)
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        songid = singer_info[1]
        songurl = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(songid)
        songname = singer_info[0]
        # path = 'D:\\code_new\\pycharm\\yunmusic\\song' + songname + '.mp3'
        down_path=path+'\\'+songname+'.mp3'
        save_song(songurl, down_path,songname)
        time.sleep(1)

def lyrics_from_singerid(id,path):              #根据歌手id下载歌词，输入为歌手id和本地保存路径
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        lyric = get_lyrics(singer_info[1])
        save2txt(singer_info[0], lyric, path)
        time.sleep(1)

def songs_from_singerid(id,path):               #根据歌手id下载歌曲音频，输入为歌手id和本地保存路径
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        songid = singer_info[1]
        songurl = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(songid)
        songname = singer_info[0]
        # path = 'D:\\code_new\\pycharm\\yunmusic\\song' + songname + '.mp3'
        down_path = path + '\\' + songname + '.mp3'
        save_song(songurl, down_path, songname)
        time.sleep(1)

#功能四：下载mv
import requests
import os
import sys
from urllib.parse import urlparse,parse_qs

def http_get(api):
    my_cookie = {
    "version":0,
    "name":'appver',
    "value":'1.5.0.75771',
    "port":None,
    # "port_specified":False,
    "domain":'www.mydomain.com',
    # "domain_specified":False,
    # "domain_initial_dot":False,
    "path":'/',
    # "path_specified":True,
    "secure":False,
    "expires":None,
    "discard":True,
    "comment":None,
    "comment_url":None,
    "rest":{},
    "rfc2109":False
    }

    s = requests.Session()
    s.headers.update({'Referer': "http://music.163.com/"})
    s.cookies.set(**my_cookie)
    response  = s.get(api)
    json_data = json.loads(response.text)
    return json_data

def download_single_mv(id):                 #根据mvid下载
    size = "720" #default 720p
    api = "http://music.163.com/api/mv/detail?id="+str(id)+"&type=mp4"
    json_data = http_get(api)
    if json_data["code"]==200:
        a = list(json_data["data"]["brs"].keys())
        if size not in a:
            size = a[0]         #如果没有720p，则选择最小的版本
        mvurl = json_data["data"]["brs"][size]      #mv网址
        artist = json_data["data"]["artistName"]    #歌手信息
        song = json_data["data"]["name"]            #歌曲信息

        filename = '%s/[%s]%s.mp4' %(artist,size,song)

        if os.path.exists(filename)==False:
            if  os.path.exists(artist)==False:
                os.makedirs(artist)
            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent = readsofar * 1e2 / totalsize
                    s = "\r%5.1f%% %*d / %d" % (
                        percent, len(str(totalsize)), readsofar, totalsize)
                    sys.stderr.write(s)
                    if readsofar >= totalsize: # near the end
                        sys.stderr.write("\n")
                else: # total size is unknown
                    sys.stderr.write("read %d\n" % (readsofar,))
            print("downloading "+filename)
            urlretrieve(mvurl,filename,reporthook)

def download_mv_from_list(url):         #批量下载歌单的mv资源
    input=url.replace("#","")
    id = parse_qs(urlparse(input).query)["id"][0]
    if "playlist" in input:
        playlist_api = "http://music.163.com/api/playlist/detail?id=%s" % (id)
        json_data = http_get(playlist_api)
        for idx, mv in enumerate(json_data["result"]["tracks"]):        #mv信息
            download_single_mv(mv["mvid"])
            print("downloaded:" + str(idx))
    elif "album" in input:
        playlist_api = "http://music.163.com/api/album/%s" % (id)
        json_data = http_get(playlist_api)
        for idx, mv in enumerate(json_data["album"]["songs"]):
            if mv["mvid"] != None and mv["mvid"] != 0:
                download_single_mv(mv["mvid"])
                print("downloaded:" + str(idx))
        download_single_mv(id)


#功能五：爬取歌曲评论并生成词云图
from jieba import posseg
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import wordcloud

def _content_generator(music_id):               #根据歌曲id获取评论信息
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_%s' % music_id
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'music.163.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': '__f_=1544879495065; _ntes_nnid=ec5f372598a44f7d45726f800d3c244b,1544879496275; _ntes_nuid=ec5f372598a44f7d45726f800d3c244b; _iuqxldmzr_=32; __utmc=94650624; WM_TID=SjPgpIfajWhEUVQQAVYoLv%2BJSutc41%2BE; __utma=94650624.1212198154.1546091705.1546142549.1546173830.4; __utmz=94650624.1546173830.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=fjy1sURvfoc29LFwx6VN7rVC6wTgq5EA1go8oNGPt2OIoPoLBInGAKxG9Rc6%2BZ%2F6HQPKefTD2kdeQesFU899HSQfRmRPbGmc6lxhGHcRpZAVtsYhGxIWtlaVLL1c0Z7HYUc%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89ef48839ff7a3f0668abc8aa3d15b938b8abab76ab6afbab4db5aacaea290c52af0fea7c3b92aa6b6b7d2f25f92aaaa90e23afb948a98fb3e9692f993d549f6a99c88f43f879fff88ee34ad9289b1f73a8d97a1b1ee488297a2a8c441bc99f7b3e23ee986e1d7cb5b9495ab87d750f2b5ac86d46fb19a9bd9bc338c8d9f87d1679290aea8f069f6b4b889c644a18ec0bbc45eb8ad9789c6748b89bc8de45e9094ff84b352f59897b6e237e2a3; __utmb=94650624.8.10.1546173830; JSESSIONID-WYYY=JhDousUg2D2BV1f%2Bvq6Ka6iQHAWfFvQOPdvf5%5CPMQISbc5nnfzqQAJDcQsezW82Cup2H5n1grdeIxXp79veCgoKA68D6CSkgCXcOFkI04Hv8hEXG9tWSMKuRx0XZ4Bp%5C%5CSbZzeRs6ey4FxADkuPVlIIVSGn%2BTq8mYstxPYBIg0f2quO%5C%3A1546177369761',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    limit = 20
    offset = 0
    compiler = re.compile(r'[^\u4E00-\u9FA5^\u3000-\u303F^\uFF00-\uFFEF^0-9^a-z^A-Z]')

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        offset += limit
        r = requests.get(url, headers=headers, params=params)
        comments = r.json()['comments']
        has_more = r.json()['more']

        for t in comments:
            yield compiler.subn('', t['content'])[0]

        if not has_more:
            break


class WangYiMusicWordCloud:             #自定义类，生成词云图
    stop_words = ['首歌']
    def __init__(self, music_id, mask=None, font_path=None, stop_words=None):
        self.music_id = music_id            #歌曲信息
        self.mask = mask                    #背景图片
        self.font_path = font_path          #字体

        if not stop_words is None:
            self.stop_words+=stop_words

        self.img_wordcloud = None

    def _cut_word(self, comment):           #分词
        word_pairs = posseg.lcut(comment, HMM=False)
        result = []
        for t in word_pairs:
            if not (t.word in result or t.word in self.stop_words):
                result.append(t.word)
        return '/'.join(result)


    def get_words_text(self):               #若已有评论文件则读取，若没有则爬取评论并保存
        if os.path.isfile(f'{self.music_id}.txt'):
            print('评论文件已存在，读取文件...')
            with open(f'{self.music_id}.txt', 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print('没有默认评论文件，开始爬取评论...')
            count = 0
            text = []
            comments = _content_generator(self.music_id)
            for t in comments:
                text.append(self._cut_word(t))

                count += 1
                print(f'\r已爬取 {count}条评论', end='')
                if count % 100 == 0:
                    print(f'\r已爬取 {count}条评论, 休息 2s', end='')
                    time.sleep(2)

            str_text = '\n'.join(text)
            with open(f'{self.music_id}.txt', 'w', encoding='utf-8') as f:
                f.write(str_text)
                print(f'\r共爬取 {count}条评论，已写入文件 {self.music_id}.txt')
            return str_text

    def generate(self, **kwargs):
        default_kwargs = {
            'background_color': "white",
            'width': 1000,
            'height': 860,
            'margin': 2,
            'max_words': 50,
            'stopwords': wordcloud.STOPWORDS,
        }
        if not self.mask is None:
            default_kwargs['mask'] = np.array(Image.open(self.mask))
        if not self.font_path is None:
            default_kwargs['font_path'] = self.font_path
        elif 'font_path' not in kwargs:
            raise ValueError('缺少参数 font_path')
        default_kwargs.update(kwargs)

        str_text = self.get_words_text()
        self.wordcloud = wordcloud.WordCloud(**default_kwargs)
        self.img_wordcloud = self.wordcloud.generate(str_text)

    def show_wordcloud(self):               #生成词云图
        if self.img_wordcloud is None:
            self.generate()

        plt.axis('off')
        plt.imshow(self.img_wordcloud)
        plt.show()

    def to_file(self, filename):            #保存到本地
        if not hasattr(self, 'wordcloud'):
            self.generate()
        self.wordcloud.to_file(filename)

def get_wordcloud(music_id,mask,font,path):         #执行函数
    wordcloud_obj = WangYiMusicWordCloud(music_id, mask=mask, font_path=font)
    wordcloud_obj.show_wordcloud()
    result=path+'\\'+'result.jpg'
    wordcloud_obj.to_file(result)


