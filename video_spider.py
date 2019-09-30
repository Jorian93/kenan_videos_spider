from urllib import request
import re
import time
import random
import datetime
import os
import requests
import utils

# 目标网站
# 定义一个类，爬虫类,self当前类

class VideoSpider():
    def __init__(self):
        """
        :param url: 源地址
        :param start: 开始地址.
        :param end: 结束地址
        :param filePath: 文件保存路径
        """
        # 读取配置文件
        config = open('spider.conf', 'r', encoding='UTF-8-sig').read()
        # 去掉\n
        config = config.strip("\n")
        # 切割
        confs = config.split(',')
        print(confs)
        # 填写配置
        self.url = confs[0]
        self.start = int(confs[1])
        self.end = int(confs[2])
        self.file_path = confs[3]

    # 获取视频地址
    def get_video_urls(self):
        # 视频列表
        video_list = []
        print(">>视频地址收集开始...")
        # 图片地址集合
        video_url = self.url
        # 读取本地代理池文件
        for i in range(self.start, self.end):
            proxy_handler = request.ProxyHandler({"http": "119.101.114.144:9999"})
            opener = request.build_opener(proxy_handler)
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'),
                ('Host', 'media2.fcw67.com'),
            ]
            request.install_opener(opener)
            req_url = request.Request(video_url + str(i + 5100))
            print('req_url:' + video_url + str(i + 5100))
            try:
                with request.urlopen(req_url, timeout=10) as f:
                    print('Status:', f.status, f.reason)
                    # for k, v in f.getheaders():
                    # print('%s: %s' % (k, v))
                    # 获取返回的页面
                    page = f.read().decode('utf-8')
                    # print('PageData:', page)
                    # 定义匹配正则表达式
                    reg = re.compile('''video_url: '(.+?)',''')
                    reg_title = re.compile('''<title>(.+?)</title>''')
                    matchs = reg.findall(page)
                    matchstitle = reg_title.findall(page)
                    # print('m:', matchstitle)
                    for row in matchs:
                        video = []
                        video_src = row
                        video_name = matchstitle[0]
                        # 名称去空格
                        video_name = video_name.replace(" ", "")
                        # 名称去/
                        video_name = video_name.replace("/", "")

                        video.append(video_name)
                        video.append(video_src)
                        video_list.append(video)
                        print('' >> +video_name + '已加入下载队列,等待下载！')
            except:
                pass
            continue
            # 一次循环后随机延迟，防止反爬虫封ip
            sleep_time = random.randint(3, 6)
            time.sleep(sleep_time)
        return video_list

    def get_real_url(self, url, try_count):
        # print("获取真实地址")
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        if try_count > 3:
            return url
        try:
            rs = requests.get(url, headers=headers, timeout=10)
            if rs.status_code > 400:
                return self.get_real_url(url, try_count + 1)
            return rs.url
        except:
            return self.get_real_url(url, try_count + 1)

    def download_video(self, video_lists):
        print(">>视频列表下载开始...")
        print(video_lists)
        x = 0
        file_path = self.file_path
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for video in video_lists:
            video_name = video[0]
            video_url = video[1]
            # 获取真实地址
            print("解析地址中...")
            real_rul = self.get_real_url(video_url, 1)
            # print("真实地址"+real_rul)
            # 现在时间戳
            now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            # 文件名为当前时间戳+视频title
            file_name = str(now_time) + '_' + video_name
            print(file_name + '开始下载...')
            request.urlretrieve(real_rul, file_path + '%s.mp4' % file_name, reporthook=utils.schedule())
            print(file_name + '下载完成...')
            x = x + 1
        print('下载完成...共' + str(x) + '个视频')
        print('视频保存地址：' + file_path)


if __name__ == "__main__":
    spider = VideoSpider()
    video_lists = spider.get_video_urls()
    print(video_lists)
    video_lists2 = [
        'http://v.stu.126.net/mooc-video/nos/mp4/2018/03/20/1008744423_c8f149213a154140ab6d98b326b33e55_shd.mp4']
    video_lists3 = ['https://newfcw.info/get_file/1/169baa4efce34add8151d50b750a659d3b3eb16228/9000/9782/9782.mp4']
    video_lists1 = [
        'https://media2.fcw67.com/remote_control.php?time=1569646161&cv=f93e21b7d053789724c640cfd04eae54&lr=0&cv2=f680e9fdb1790f2f0424a9766cf11a6e&file=%2Fvideos%2F9000%2F9782%2F9782.mp4']
    spider.download_video(video_lists)
