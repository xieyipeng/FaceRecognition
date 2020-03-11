# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from twisted.test.test_threads import cls


class TextPipeline(object):

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
                return item
            pass
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(self, crawler):
        return cls(
            mongo_uri=crawler.settings.get('Mongo_uri'),
            mongo_db=crawler.settings.get('Mongo_db')
        )

    def open_spider(self, spider):
        # self.client=pymogo
        pass

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        # self.client.close()
        pass
