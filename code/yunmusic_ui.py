from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import csv

def single_song():                  #下载单一歌曲
    song_id=entry2_id.get()
    song_name=entry2_name.get()
    path=entry2_path.get()
    song_url = "http://music.163.com/song/media/outer/url?id=%s" % song_id
    down_path = path + '\\' + song_name + '.mp3'
    urlretrieve(song_url,down_path)
    text.insert(END,"downloading song：%s" % song_name)
    text.see(END)
    text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

def single_song_lyric():            #下载单一歌曲的歌词
    id=entry2_id.get()
    name=entry2_name.get()
    path=entry2_path.get()
    text.insert(END, "downloading lyric：%s" % name)
    text.see(END)
    text.update()
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(id)
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    json_obj = json.loads(html)
    initial_lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lyric = re.sub(reg, '', initial_lyric).strip()
    save2txt(name,lyric,path)
    time.sleep(1)

    text.insert(END, "Finished!")
    text.see(END)
    text.update()



def songs_from_list():            #url:歌单网址；path:本地保存目录
    url=entry1_list.get()
    path=entry1_path.get()
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
        down_path=path+ '\\' +music_dict[song_id]+'.mp3'

        # path = "C:\\Users\\ming-\\Downloads\\%s.mp3" % music_dict[song_id]

        # 添加数据
        text.insert(END,"downloading song：%s" % music_dict[song_id])
        text.see(END)
        text.update()

        urlretrieve(song_url, down_path)
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

def get_id(singer_name):
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

# 根据歌手姓名获取歌词
import json
import time
def get_html(url):          #通过代理ip获取网页信息
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

def get_top50(html):                 #获取热度前50名的歌曲，并返回对应的歌曲名称和歌曲id，输入为歌手详情页
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

def get_lyrics(songids):
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

def save2txt(songname, lyric,path):         #保存歌词文件到本地
    print('正在保存歌曲：{}'.format(songname))
    lyric_path=path+ '\\' +songname+'.txt'
    with open(lyric_path, 'a', encoding='utf-8')as f:
        f.write(lyric)

def lyrics_from_singer():
    name=entry3_name.get()
    path=entry3_path.get()

    id=get_id(name)
    text.insert(END, "singer_id：%s" % id)
    text.see(END)
    text.update()

    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        lyric = get_lyrics(singer_info[1])
        save2txt(singer_info[0], lyric, path)
        time.sleep(1)

        text.insert(END, "downloading lyrics：%s" % singer_info[0])
        text.see(END)
        text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

def lyrics_from_singer_id():
    id=entry3_id.get()
    path=entry3_path.get()
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)
    for singer_info in singer_infos:
        lyric = get_lyrics(singer_info[1])
        save2txt(singer_info[0], lyric, path)
        time.sleep(1)

        text.insert(END, "downloading lyrics：%s" % singer_info[0])
        text.see(END)
        text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

import urllib
def save_song(songurl, path,songname):
    try:
        urllib.request.urlretrieve(songurl, path)
        print('歌曲下载完成：' + songname)
    except BaseException:
        print('下载失败：' + songname)
        pass

def song_from_singer():
    name=entry3_name.get()
    path=entry3_path.get()
    id=get_id(name)
    top50url = 'https://music.163.com/artist?id={}'.format(id)
    html = get_html(top50url)
    singer_infos = get_top50(html)

    text.insert(END, "singer_id：%s" % id)
    text.see(END)
    text.update()

    for singer_info in singer_infos:
        songid = singer_info[1]
        songurl = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(songid)
        songname = singer_info[0]
        # path = 'D:\\code_new\\pycharm\\yunmusic\\song' + songname + '.mp3'
        down_path=path+ '\\'+ songname+'.mp3'
        save_song(songurl, down_path,songname)
        time.sleep(1)

        text.insert(END, "downloading song：%s" % songname)
        text.see(END)
        text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

def song_from_singer_id():
    id=entry3_id.get()
    path=entry3_path.get()
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

        text.insert(END, "downloading song：%s" % songname)
        text.see(END)
        text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

def lyrics_from_list():                 #根据歌单下载歌曲歌词
    url=entry1_list.get()
    path=entry1_path.get()
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
        text.insert(END, "downloading lyrics：%s" % music_dict[i])
        text.see(END)
        text.update()
    text.insert(END, "Finished!")
    text.see(END)
    text.update()

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
            size = a[0]
        mvurl = json_data["data"]["brs"][size]
        artist = json_data["data"]["artistName"]
        song = json_data["data"]["name"]

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

                    text.insert(END, s)
                    text.see(END)

                    text.after(1, text.update())
                    text.delete(END, END)

                    if readsofar >= totalsize: # near the end
                        sys.stderr.write("\n")
                else: # total size is unknown
                    sys.stderr.write("read %d\n" % (readsofar,))
            print("downloading "+filename)

            text.insert(END, "downloading "+filename)
            text.see(END)
            text.update()

            urlretrieve(mvurl,filename,reporthook)

def download_single_mv_tkinter():
    id=entry4_id.get()
    size = "720" #default 720p
    api = "http://music.163.com/api/mv/detail?id="+str(id)+"&type=mp4"
    json_data = http_get(api)
    if json_data["code"]==200:
        a = list(json_data["data"]["brs"].keys())
        if size not in a:
            size = a[0]
        mvurl = json_data["data"]["brs"][size]
        artist = json_data["data"]["artistName"]
        song = json_data["data"]["name"]

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

                    text.insert(END, s)
                    text.see(END)

                    text.after(1,text.update())
                    text.delete(END, END)

                    if readsofar >= totalsize: # near the end
                        sys.stderr.write("\n")
                else: # total size is unknown
                    sys.stderr.write("read %d\n" % (readsofar,))
            print("downloading "+filename)
            text.insert(END, "downloading "+filename)
            text.see(END)
            text.update()
            urlretrieve(mvurl,filename,reporthook)


def download_mv_from_list():        #批量下载歌单的mv资源
    url=entry4_url.get()
    input=url.replace("#","")
    id = parse_qs(urlparse(input).query)["id"][0]
    if "playlist" in input:
        playlist_api = "http://music.163.com/api/playlist/detail?id=%s" % (id)
        json_data = http_get(playlist_api)
        for idx, mv in enumerate(json_data["result"]["tracks"]):
            download_single_mv(mv["mvid"])
            print("downloaded:" + str(idx))

            text.insert(END, "downloaded:" + str(idx))
            text.see(END)
            text.update()

    elif "album" in input:
        playlist_api = "http://music.163.com/api/album/%s" % (id)
        json_data = http_get(playlist_api)
        for idx, mv in enumerate(json_data["album"]["songs"]):
            if mv["mvid"] != None and mv["mvid"] != 0:
                download_single_mv(mv["mvid"])
                print("downloaded:" + str(idx))

                text.insert(END, "downloaded:" + str(idx))
                text.see(END)
                text.update()

        download_single_mv(id)



#功能五：爬取歌曲评论并生成词云图
from jieba import posseg
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import wordcloud

def _content_generator(music_id):           #根据歌曲id获取评论信息
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
    limit = 10
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

    def _cut_word(self, comment):
        word_pairs = posseg.lcut(comment, HMM=False)
        result = []
        for t in word_pairs:
            if not (t.word in result or t.word in self.stop_words):
                result.append(t.word)
        return '/'.join(result)


    def get_words_text(self):            #若已有评论文件则读取，若没有则爬取评论并保存
        # global flag = 0
        if os.path.isfile(f'{self.music_id}.txt'):
            # flag=1
            print('评论文件已存在，读取文件...')

            # text.insert(END, '评论文件已存在，读取文件...')
            # text.see(END)
            # text.update()


            with open(f'{self.music_id}.txt', 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # flag=2
            print('没有默认评论文件，开始爬取评论...')

            # text.insert(END, '没有默认评论文件，开始爬取评论...')
            # text.see(END)
            # text.update()


            count = 0
            text = []
            comments = _content_generator(self.music_id)
            for t in comments:
                text.append(self._cut_word(t))

                count += 1
                print(f'\r已爬取 {count}条评论', end='')

                # text.insert(END, "test")
                # text.see(END)
                # text.update()

                if count % 100 == 0:
                    print(f'\r已爬取 {count}条评论, 休息 2s', end='')
                    time.sleep(2)

            str_text = '\n'.join(text)
            with open(f'{self.music_id}.txt', 'w', encoding='utf-8') as f:
                f.write(str_text)
                print(f'\r共爬取 {count}条评论，已写入文件 {self.music_id}.txt')

                # text.insert(END, f'\r共爬取 {count}条评论，已写入文件 {self.music_id}.txt')
                # text.see(END)
                # text.update()

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

    def show_wordcloud(self):            #生成词云图
        if self.img_wordcloud is None:
            self.generate()

        plt.axis('off')
        plt.imshow(self.img_wordcloud)
        plt.show()

    def to_file(self, filename):        #保存在本地
        if not hasattr(self, 'wordcloud'):
            self.generate()
        self.wordcloud.to_file(filename)

def get_wordcloud():
    music_id=entry5_id.get()
    mask=entry5_mask.get()
    font=entry5_font.get()
    wordcloud_obj = WangYiMusicWordCloud(music_id, mask=mask, font_path=font)

    text.insert(END, 'getting comments,please wait')
    text.see(END)
    text.update()


    wordcloud_obj.show_wordcloud()

    text.insert(END, 'finished analysing comments')
    text.see(END)
    text.update()
    text.insert(END,'picture has been saved')
    text.see(END)
    text.update()
    result='result.jpg'
    wordcloud_obj.to_file(result)


# 界面
from tkinter.filedialog import askdirectory,askopenfilename

def selectpath1():          #调用资源管理器
    path_=askdirectory()
    path1.set(path_)

def selectpath2():
    path_=askdirectory()
    path2.set(path_)

def selectpath3():
    path_=askdirectory()
    path3.set(path_)

def selectfile4():
    filename=askopenfilename()
    path4.set(filename)

def selectfile5():
    filename=askopenfilename()
    path5.set(filename)

from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("yunmusic downloader")
root.geometry("750x650")

path1=StringVar()
path2=StringVar()
path3=StringVar()
path4=StringVar()
path5=StringVar()


Label(root,text="Download songs in lists:",font=('楷体',15)).place(x=10,y=10)
Label(root,text="list url",font=('微软雅黑',12)).place(x=10,y=45)
Label(root,text="path",font=('微软雅黑',12)).place(x=10,y=70)

entry1_list=Entry(root,font=('微软雅黑', 12),width=30)
entry1_list.place(x=70,y=45)
entry1_path=Entry(root,textvariable=path1,font=('微软雅黑', 12),width=26)
entry1_path.place(x=70,y=70)

butt1_path=Button(root, text="select", font=("微软雅黑", 7), command=selectpath1)
butt1_path.place(x=310,y=70)

button1 = Button(root, text="download songs", font=("微软雅黑", 10), command=songs_from_list)
button1.place(x=30,y=100)
button1_lyric=Button(root, text ="download lyrics", font=("微软雅黑", 10), command=lyrics_from_list)
button1_lyric.place(x=230,y=100)

Label(root,text="Download song with id:",font=('楷体',15)).place(x=10,y=140)
Label(root,text="song name",font=('微软雅黑',12)).place(x=10,y=175)
Label(root,text="id",font=('微软雅黑',12)).place(x=10,y=200)
Label(root,text="path",font=('微软雅黑',12)).place(x=10,y=225)



entry2_name=Entry(root,font=('微软雅黑', 12),width=24)
entry2_name.place(x=124,y=175)
entry2_id=Entry(root,font=('微软雅黑', 12),width=30)
entry2_id.place(x=70,y=200)
entry2_path=Entry(root,textvariable=path2,font=('微软雅黑', 12),width=26)
entry2_path.place(x=70,y=225)


butt2_path=Button(root, text="select", font=("微软雅黑", 7), command=selectpath2)
butt2_path.place(x=310,y=225)

button2=Button(root, text="download song", font=("微软雅黑", 10), command=single_song)
button2.place(x=30,y=255)
button2_lyric=Button(root, text="download lyric", font=("微软雅黑", 10), command=single_song_lyric)
button2_lyric.place(x=230,y=255)

Label(root,text="Download songs by singer:",font=('楷体',15)).place(x=10,y=300)
Label(root,text="singer name",font=('微软雅黑',12)).place(x=10,y=335)
Label(root,text="singer id",font=('微软雅黑',12)).place(x=10,y=360)
Label(root,text="path",font=('微软雅黑',12)).place(x=10,y=385)

entry3_name=Entry(root,font=('微软雅黑', 12),width=24)
entry3_name.place(x=124,y=335)
entry3_id=Entry(root,font=('微软雅黑', 12),width=24)
entry3_id.place(x=124,y=360)
entry3_path=Entry(root,textvariable=path3,font=('微软雅黑', 12),width=26)
entry3_path.place(x=70,y=385)

butt3_path=Button(root, text="select", font=("微软雅黑", 7), command=selectpath3)
butt3_path.place(x=310,y=385)

button3 = Button(root, text="download songs by name", font=("微软雅黑", 10), command=song_from_singer)
button3.place(x=30,y=415)
button3_lyric=Button(root, text ="download lyrics by name", font=("微软雅黑", 10), command=lyrics_from_singer)
button3_lyric.place(x=230,y=415)

butt3_lyrics=Button(root, text ="download lyrics by id", font=("微软雅黑", 10), command=lyrics_from_singer_id)
butt3_lyrics.place(x=230,y=450)

butt3_songs=Button(root, text ="download songs by id", font=("微软雅黑", 10), command=song_from_singer_id)
butt3_songs.place(x=30,y=450)


Label(root,text="Download mv:",font=('楷体',15)).place(x=10,y=500)
Label(root,text="mv id",font=('微软雅黑',12)).place(x=10,y=535)
Label(root,text="list url",font=('微软雅黑',12)).place(x=10,y=560)
entry4_id=Entry(root,font=('微软雅黑', 12),width=30)
entry4_id.place(x=70,y=535)
entry4_url=Entry(root,font=('微软雅黑', 12),width=30)
entry4_url.place(x=70,y=560)
butt4=Button(root,text="Download single mv",font=("微软雅黑", 10), command=download_single_mv_tkinter)
butt4_list=Button(root,text="Download mv in lists",font=("微软雅黑", 10), command=download_mv_from_list)
butt4.place(x=30,y=590)
butt4_list.place(x=230,y=590)

Label(root,text="Get wordcloud:",font=('楷体',15)).place(x=410,y=10)
Label(root,text="song id",font=('微软雅黑',12)).place(x=410,y=45)
Label(root,text="mask",font=('微软雅黑',12)).place(x=410,y=70)
Label(root,text="font",font=('微软雅黑',12)).place(x=410,y=95)

entry5_id=Entry(root,font=('微软雅黑', 12),width=25)
entry5_id.place(x=480,y=45)
entry5_mask=Entry(root,textvariable=path4,font=('微软雅黑', 12),width=20)
entry5_mask.place(x=480,y=70)
entry5_font=Entry(root,textvariable=path5,font=('微软雅黑', 12),width=20)
entry5_font.place(x=480,y=95)

butt5_path_mask=Button(root, text="select", font=("微软雅黑", 7), command=selectfile4)
butt5_path_mask.place(x=675,y=70)
butt5_path_mask=Button(root, text="select", font=("微软雅黑", 7), command=selectfile5)
butt5_path_mask.place(x=675,y=95)

butt5=Button(root,text="Get wordcloud",font=("微软雅黑", 10), command=get_wordcloud)
butt5.place(x=600,y=130)

text = Listbox(root, font=("微软雅黑", 10), width=40, height=21)
text.place(x=400,y=200)



mainloop()