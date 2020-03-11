# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest


class WeiboSpider(Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    search_url = 'https://weibo.cn/search/mblog'
    max_page = 100

    def start_requests(self):
        keyword = '000001'
        url = '{url}?keyword={keyword}'.format(url=self.search_url, keyword=keyword)
        for page in range(self.max_page + 1):
            data = {
                'mp': str(self.max_page),
                'page': str(page)
            }
            yield FormRequest(url=url, callback=self.parse_index, formdata=data)

    def parse(self, response):
        pass

    def parse_index(self, response):
        print(response.text)
