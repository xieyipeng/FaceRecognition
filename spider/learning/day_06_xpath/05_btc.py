import requests
from lxml import etree
import json


class BtcSpider(object):
    def __init__(self):
        # self.base_url = 'https://www.8btc.com/'
        self.base_url = 'http://www.5nj.com/index.php?m=vod-list-id-6-pg-'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }

    # 1.发送求
    def get_response(self, url):
        return requests.get(url, headers=self.headers).content.decode('utf-8')

    # 2.解析数据
    def parse_data(self, data):
        web = 'http://www.5nj.com'
        # 使用xpath解析当前页面所有新闻title和url保存
        x_data = etree.HTML(data)
        res_title = x_data.xpath('//div[@class="face front"]//a[@class="link-hover"]/@title')
        res_href = x_data.xpath('//div[@class="face front"]//a[@class="link-hover"]/@href')
        data_list = []
        for index, title in enumerate(res_title):
            movies = {}
            movies['name'] = title
            movies['url'] = web + res_href[index]
            data_list.append(movies)
        return data_list

    # 3.保存数据
    @staticmethod
    def save_my_data(data):
        # list->str
        data_str = json.dumps(data)
        with open('05_btc.json', 'w', encoding='utf-8')as f:
            f.write(data_str)

    # 4.启动
    def run(self):
        # 1.拼接完整的url
        page = '1'
        red = '-order--by-time-class-0-year-0-letter--area--lang-.html'
        url = self.base_url + page + red
        # print(url)

        # 2.发请求
        data = self.get_response(url)

        # 3.做解析
        parse_data = self.parse_data(data)

        # 4.保存
        self.save_my_data(parse_data)


BtcSpider().run()
