import requests
from bs4 import BeautifulSoup
from lxml import etree
import json


class BookSpider(object):
    def __init__(self):
        self.base_url = 'http://www.allitebooks.org/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        self.page_num = self.get_page_num()
        self.data_list = []

    # 0.获取总页数
    def get_page_num(self):
        url = 'http://www.allitebooks.org/'
        HomePage_data = requests.get(url, headers=self.headers).content.decode('utf-8')
        soup = BeautifulSoup(HomePage_data, 'lxml')
        return soup.select('a[title="Last Page →"]')[0].get_text()

    # 1.构建所有的url
    def get_url_list(self):
        url_list = []
        for i in range(1, 11):
            url = self.base_url.format(i)
            url_list.append(url)

        return url_list

    # 2.发送请求
    def send_request(self, url):
        print(url)
        data = requests.get(url, headers=self.headers).content.decode('utf-8')
        return data

    # 3.解析数据 xpath
    def parse_xpath_data(self, data):
        parse_data = etree.HTML(data)
        # 解析所有的书
        book_list = parse_data.xpath('//div[@class="main-content-inner clearfix"]/article')
        # 解析出每一本书的信息
        for book in book_list:
            book_dict = {}
            # 1.书名
            book_dict['book_name'] = book.xpath('.//h2[@class="entry-title"]//text()')
            # 2.图片url
            book_dict['book_img_url'] = book.xpath('./div[@class="entry-thumbnail hover-thumb"]/a/img/@src')
            # 3.作者
            book_dict['book_author'] = book.xpath('.//h5[@class="entry-author"]/a/text()')
            # 4.简介
            book_dict['book_info '] = book.xpath('.//div[@class="entry-summary"]/p/text()')
            self.data_list.append(book_dict)

    def parse_bs4_data(self, data):
        parse_data = etree.HTML(data)
        # 解析所有的书
        soup = BeautifulSoup(data, 'lxml')
        book_list = soup.select('article')

        # 解析出每一本书的信息
        for book in book_list:
            book_dict = {}
            # 1.书名
            book_dict['book_name'] = book.select_one('.entry-title').get_text()
            # 2.图片url
            book_dict['book_img_url'] = book.select_one('.attachment-post-thumbnail').get('src')
            # 3.作者
            book_dict['book_author'] = book.select_one('.entry-author').get_text()[4:]
            # 4.简介
            book_dict['book_info '] = book.select_one('.entry-summary p').get_text()
            self.data_list.append(book_dict)

    # 4.保存
    def save_data(self):
        json.dump(self.data_list, open('04_ebook.json', 'w', encoding='utf-8'))

    # 统筹调用
    def start(self):
        url_list = self.get_url_list()
        # 循环发送请求
        for url in url_list:
            data = self.send_request(url)
            self.parse_bs4_data(data)
        print(self.data_list)
        self.save_data()


BookSpider().start()
