# -*- coding: utf-8 -*-
import scrapy
import json

from ..items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'arcbai-jia'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'ad_type,available_message_types,default_notifications_count,follow_notifications_count,vote_thank_notifications_count,messages_count,account_status,email,is_bind_phone'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(user=self.start_user, include=self.user_query),
                             callback=self.parse_user)

        yield scrapy.Request(
            url=self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
            callback=self.parse_follows)

        yield scrapy.Request(
            url=self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
            callback=self.parse_followers)

    def parse(self, response):
        print(response.text)

    def parse_user(self, response):
        res = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in res.keys():
                item[field] = res.get(field)
        print(item)
        yield item

        print('yield')

        yield scrapy.Request(
            self.follows_url.format(user=res.get('url_token'), include=self.follows_query, limit=20, offset=0),
            self.parse_follows)
        yield scrapy.Request(
            self.followers_url.format(user=res.get('url_token'), include=self.followers_query, limit=20, offset=0),
            self.parse_followers)

    def parse_follows(self, response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for re in res.get('data'):
                yield scrapy.Request(self.user_url.format(user=re.get('url_token'), include=self.user_query),
                                     callback=self.parse_user)
        if 'paging' in res.keys() and res.get('paging').get('is_end') is False:
            next_page = res.get('paging').get('next')
            yield scrapy.Request(url=next_page, callback=self.parse_follows)

    def parse_followers(self, response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for re in res.get('data'):
                yield scrapy.Request(self.user_url.format(user=re.get('url_token'), include=self.user_query),
                                     callback=self.parse_user)
        if 'paging' in res.keys() and res.get('paging').get('is_end') is False:
            next_page = res.get('paging').get('next')
            yield scrapy.Request(url=next_page, callback=self.parse_followers)
