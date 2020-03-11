# -*- coding: utf-8 -*-
import scrapy


class FanyiSpider(scrapy.Spider):
    name = 'fanyi'
    allowed_domains = ['http://fanyi.youdao.com/']
    start_urls = ['http://fanyi.youdao.com//']

    def parse(self, response):
        print(response.text)
