# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twiter_scraper.items import Tweet, User

class TwiterScraperPipeline(object):
    def process_item(self, item, spider):
        return item


class RethinkDBSaver(object):
    
