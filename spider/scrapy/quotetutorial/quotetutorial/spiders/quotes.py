# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').get()
            author = quote.css('.author::text').get()
            tags = quote.css('.tags .tag::text').getall()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').get()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
