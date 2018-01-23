# -*- coding: utf-8 -*-
import json
import logging

import scrapy
from scrapy import http

from twiter_scraper.parser import parse_tweets, parse_users

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

logger = logging.getLogger(__name__)

# TODO create proxy handler


class TweetCrawlerSpider(scrapy.Spider):
    name = 'tweet_crawler'
    allowed_domains = ['www.twiter.com']
    # TODO f=tweets can be change for vertical etc
    URL = r"https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"
    user_popup_url = "https://twitter.com/i/profiles/popup?user_id=%d"

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
        TODO create scrapy contracts
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

        self.search_params = {
            "query": query,
            "lang": lang,
            "max_tweets": max_tweets,
            "since": since,
            "until": until,
            "top_tweets": top_tweets,
            "user_name": user_name,
            "near": near,
            "within": within
        }

        self.start_urls = [self.create_query(refresh_cursor='')]

        pass

    def create_query(self, refresh_cursor):
        '''create_query use the params from the constructor
        to create the inital query and set the start url'''
        url = self.URL
        # TODO this maybe can be beneficial for top_tweets
        # if not top_tweets:
        #     url = url + "&f=tweets"

        # url = url + "&q=%s&src=typed&max_position=%s"
        #
        q = ''
        if self.search_params['user_name']:
            q += 'from:' + self.search_params['user_name']
            logger.debug("Adding user to start url")
        if self.search_params['since']:
            q += 'since:' + self.search_params['since']
            logger.debug("Adding since to start url")
        if self.search_params['until']:
            q += 'until:' + self.search_params['until']
            logger.debug("Adding until to start url")
        if self.search_params['query']:
            q += self.search_params['query']
            logger.debug("query: %s" % q)
        else:
            # here I need to raise a no query exception
            q = 'bitcoin'
            logger.warning("There is no query specified using 'bitcoin'")

        options = 'lang="' + self.search_params['lang'] + '"&'
        url = url % (quote(q), options, refresh_cursor)
        logger.info("Start_url: %s" % url)
        return url

    def parse(self, response):
        logger.debug("Parsing Response")
        json_response = json.loads(response.text)

        for item in parse_tweets(json_response['items_html']):
            logger.debug("Item retrieved")
            logger.debug("Requesting User")
            http.Request(
                self.user_popup_url.format(item.Id), callback=parse_users)
            yield item

        refresh_cursor = json_response['min_position']
        new_url = self.create_query(refresh_cursor)
        logger.debug("New URL: %s" % new_url)

        yield http.Request(new_url, callback=self.parse)
