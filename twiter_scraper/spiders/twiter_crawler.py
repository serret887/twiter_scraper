# -*- coding: utf-8 -*-
import scrapy


class TwiterCrawlerSpider(scrapy.Spider):
    name = 'twiter_crawler'
    allowed_domains = ['www.twiter.com']
    start_urls = ['http://www.twiter.com/']

    def parse(self, response):
        pass
