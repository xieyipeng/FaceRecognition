# -*- coding: utf-8 -*-
import scrapy
import json


class DetialSpider(scrapy.Spider):
    name = 'detial'
    allowed_domains = ['http://cdb9.com/type-38-2-1.html']

    start_urls = []

    with open("item.json", 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    for item in json_data:
        start_urls.append(item.get('url'))

    print(start_urls)


    def parse(self, response):
        pass
