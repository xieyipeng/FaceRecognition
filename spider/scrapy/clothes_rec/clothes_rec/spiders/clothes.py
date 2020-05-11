# -*- coding: utf-8 -*-
import scrapy
import json

data = []


class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['http://cdb9.com/type-38-2-1.html']
    start_urls = ['http://cdb9.com/type-38-2-4.html']

    # def start_requests(self):
    #     urls = [
    #         'http://cdb9.com/type-38-2-1.html',
    #         'http://cdb9.com/type-38-2-2.html',
    #         'http://cdb9.com/type-38-2-3.html',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file_name = 'item4.json'
        for index in range(1, 20):
            print(index)
            url = 'http://cdb9.com/' + response.xpath(
                '//*[@id="waterfall"]/li[' + str(index) + ']/div[1]/a/@href').get()
            title = response.xpath('//*[@id="waterfall"]/li[' + str(index) + ']/div[1]/a/@title').get()
            title_image = 'http://cdb9.com/' + response.xpath(
                '//*[@id="waterfall"]/li[' + str(index) + ']/div[1]/a/img/@src').get()
            author = response.xpath('//*[@id="waterfall"]/li[' + str(index) + ']/div[2]/a[1]/text()').get()


            item = {'url': url,
                    'title': title,
                    'title_image': title_image,
                    'author': author
                    }
            data.append(item)

        json_data = json.dumps(data)

        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(json_data)
