import scrapy

"""
官网例子
"""


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    start_urls = ['http://quotes.toscrape.com/page/1/']

    # 列表推导式
    # start_urls = [f'http://quotes.toscrape.com/page/{page}/' for page in range(1,11)]

    # 解析函数 response 响应源码
    def parse(self, response):
        # 选择出数据 css
        for selector in response.css('div.quote'):
            # 选择名言
            text = selector.css('span.text::text').get()
            # 选择作者
            author = selector.xpath('span/small/text()').get()
            # 返回数据 如果想保存数据，必须返回
            # 数据格式目前必须是字段格式 后期：item
            items = {
                "quote": text,
                "author": author
            }
            yield items

        # 翻页处理
        # 1.先找到下一页的网址
        # 2.发出请求，获取响应，交给parse函数
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            # 法一
            # url = 'http://quotes.toscrape.com' + next_page
            # yield scrapy.Request(url)
            # 法二
            # yield response.follow(next_page)

            yield response.follow(next_page, callback=self.parse)
