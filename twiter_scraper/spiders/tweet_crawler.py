# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy import http

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

logger = logging.getLogger(__name__)

#TODO create proxy handler


class TweetCrawlerSpider(scrapy.Spider):
    name = 'tweet_crawler'
    allowed_domains = ['www.twiter.com']
    # TODO f=tweets can be change for vertical etc
    URL = "https://twitter.com/i/search/timeline?\
    f=tweets&q=%s&src=typd&%smax_position=%s"

    def __init__(self,
                 query='',
                 lang='eng',
                 max_tweets=1,
                 since='',
                 until='',
                 top_tweets='',
                 user_name='',
                 near='',
                 within=''):
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
        logger.debug("STARTING TWEET SPIDER")
        self.create_query(query, lang, since, until, user_name)

        pass

    def create_query(self, query, lang, since, until, user_name):
        '''create_query use the params from the constructor
        to create the inital query and set the start url'''
        url = self.URL
        # if not top_tweets:
        #     url = url + "&f=tweets"

        # url = url + "&q=%s&src=typed&max_position=%s"
        #
        q = ''
        if user_name:
            q += 'from:' + user_name
        if since:
            q += 'since:' + since
        if until:
            q += 'until:' + until
        q += query
        options = 'lang=' + lang
        url = url % (quote(q), options)
        logger.debug("Start_url:", url)

    def start_request(self):
        url = self.URL
        yield http.Request(url, callback=self.parse_page)

    def parse(self, response):
        pass
