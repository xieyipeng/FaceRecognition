from lxml import etree
from bs4 import BeautifulSoup
import json
import requests


# TODO: 模糊搜索

class BtcSpider(object):
    def __init__(self):
        self.base_url = 'http://www.5nj.com/index.php?m=vod-list-id-6-pg-'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }

    # 1.发送求
    def get_response(self, url):
        return requests.get(url, headers=self.headers).content.decode('utf-8')

    # 2.解析数据
    def parse_data(self, data, rule):
        html_data = etree.HTML(data)
        # 模糊查询
        # res_list = html_data.xpath('//div[contains(@class,"container")]')
        # print(len(res_list))
        # print(res_list)

        # following-sibling::* -- 平级兄弟标签
        res_list = html_data.xpath('//head/following-sibling::*[1]')
        print(res_list)


    # 3.保存数据
    @staticmethod
    def save_my_data(data):
        with open('03_btc_bs4.html', 'w', encoding='utf-8')as f:
            f.write(data)

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
        self.parse_data(data, 1)

        # 4.保存
        # self.save_my_data(parse_data)
        # self.save_my_data(data)


BtcSpider().run()
