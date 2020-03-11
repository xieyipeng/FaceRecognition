# -*- coding: utf-8 -*-
import scrapy


class HttpbingSpider(scrapy.Spider):
    name = 'httpbing'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/post']

    def start_requests(self):
        yield scrapy.Request(url='http://httpbin.org/post', method='POST', callback=self.parse_post)

    def parse(self, response):
        pass

    def parse_post(self, response):
        print('hello',response.state)
