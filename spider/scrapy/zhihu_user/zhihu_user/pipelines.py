# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class ZhihuUserPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection_name = 'user'

    def __init__(self):
        self.client=pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['zhihu']
        self.table=self.db['user']

    def process_item(self, item, spider):
        # self.table['user'].update({'name': item['name']}, {'$set': item}, True)
        self.table[self.collection_name].insert_one(dict(item))
        return item
