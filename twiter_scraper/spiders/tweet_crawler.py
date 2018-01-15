# -*- coding: utf-8 -*-
import logging

import scrapy

logger = logging.getLogger(__name__)

#TODO create proxy handler


class TweetCrawlerSpider(scrapy.Spider):
    name = 'tweet_crawler'
    allowed_domains = ['www.twiter.com']
    start_urls = [
        'https://twitter.com/i/search/timeline?f=tweets&q=%s\
        &src=typd&%smax_position=%s'
    ]

    def __init__(self,
                 query='',
                 lang='eng',
                 max_tweets=1,
                 since='',
                 until='',
                 top_tweets='',
                 user_name='',
                 near=''):
        '''
        TODO: create the explanation of this crawler
        @query= specify the search query
        @lang=eng by default
        @max_tweets=maximum amount of tweets to retrieve
        @since=start point for the retrieval process
        @until=start point for the retrieval process
        @top_tweets=TODO// create documentation for this case
        @user_name=User name for search the tweets
        @near=Near where "location"
        @within=A distance radius between "near" location "20mi"
'''

        pass

    def parse(self, response):
        pass
