# -*- coding: utf-8 -*-
import scrapy

#添加代理


class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['http://fanyi.youdao.com/']
    start_urls = ['http://fanyi.youdao.com/']

    def parse(self, response):
        print(response.text)

