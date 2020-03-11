from bs4 import BeautifulSoup
import json
import requests
import time


# TODO: 模糊搜索

class BtcSpider(object):
    def __init__(self):
        self.base_url = 'http://www.5nj.com/index.php?m=vod-list-id-6-pg-'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        self.data_list = []

    # 1.发送求
    def get_response(self, url):
        return requests.get(url, headers=self.headers).content.decode('utf-8')

    # 2.解析数据
    def parse_list_data(self, data):
        # 1.转类型
        soup = BeautifulSoup(data, 'lxml')

        # 2.解析内容
        web = 'http://www.5nj.com'
        title_list = soup.select('.link-hover')
        for title in title_list:
            list = {}
            list['title'] = title.get('title')
            list['url'] = web + title.get('href')
            if list not in self.data_list:
                self.data_list.append(list)

        print(self.data_list)

    def parse_detail_data(self, data, i):
        soup = BeautifulSoup(data, 'lxml')
        # 取出评论
        comments = soup.select('.con')
        for comment in comments:
            print(format(i) + ' - ' + comment.get_text())

    # 3.保存数据
    @staticmethod
    def save_my_data(data, file_path):
        json_str = json.dumps(data)
        with open(file_path, 'w', encoding='utf-8')as f:
            f.write(json_str)

    # 4.启动
    def run(self):
        for i in range(1, 2):
            page = format(i)
            red = '-order--by-time-class-0-year-0-letter--area--lang-.html'
            url = self.base_url + page + red
            data = self.get_response(url)
            self.parse_list_data(data)
        # self.save_my_data(self.data_list, '04_list.json')

        # 发送详情页的请求
        i = 1
        for data in self.data_list:
            print('sleep...')
            time.sleep(2)
            detail_url = data['url']
            detail_data = self.get_response(detail_url)
            # 解析详情页数据
            self.parse_detail_data(detail_data, i)
            i = i + 1


BtcSpider().run()
