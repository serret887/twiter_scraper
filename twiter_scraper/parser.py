# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Selector
from twiter_scraper.items import Tweet, User


def parse_tweets(html_tweets):
    logger = logging.getLogger("Parser.Tweet")

    tweet_list = Selector(text=html_tweets).xpath('//li[@data-item-id]')
    for t in tweet_list:
        tweet = Tweet()
        tweet["Id"] = t.xpath('.//@data-tweet-id').extract_first()
        tweet["user_name"] = t.xpath(
            './/span[contains(@class,"username")]/b/text()').extract_first()

        tweet["user_id"] = t.xpath(
            './/a[@data-user-id]/@data-user-id').extract_first()

        # TODO: convert to UTC
        date = t.xpath('.//span/@data-time').extract_first()
        tweet["created_date"] = datetime.fromtimestamp(
            int(date)).strftime('%Y-%m-%d %H:%M:%S')

        tweet["permanent_link"] = t.xpath(
            './/@data-permalink-path').extract_first()

        # content extraction
        tweet["text"] = ' '.join(
            t.xpath('.//div[contains(@class, "text")]//text()')
            .extract()).strip().replace('\n', '')
        # TODO fixing problems with URLs inside the text

        stats = t.xpath(
            './/span[contains(@class, "actionCount")]/span/text()').extract()

        # #TODO mayber use some contains here
        for stat in stats[:3]:
            v, k = stat.strip().split()
            k = k.lower()
            if "repl" in k:
                k = "replies_amount"
            if "lik" in k:
                k = "likes_amount"
            if "retwe" in k:
                k = "retweets_amount"
            tweet[k] = v if v else 0

        # get photo
        tweet["images"] = t.xpath(".//*/div/@data-image-url").extract()
        tweet["cards"] = t.xpath('.//*/div/@data-card-url').extract()
        logger.info("Tweet parsed {}".format(tweet["Id"]))
        logger.debug(repr(tweet.__dict__))
        yield tweet


def parse_users(response):
    logger = logging.getLogger("Parser.User")

    json_response = json.loads(response.text)
    user = User()
    user["Id"] = json_response["user_id"]
    user["user_name"] = json_response["screen_name"]

    html = Selector(text=json_response["html"])

    user["name"] = ''.join(
        html.xpath('.//a[contains(@class, "fullname")]//text()')
        .extract()).strip()
    user["description"] = html.xpath(
        './/p[contains(@class, "bio")]/text()').extract_first()

    stats = html.xpath(
        './/a[contains(@class,"ProfileCardStats-statLink")]/@title').extract()

    for stat in stats[:3]:
        v, k = stat.strip().split()
        k = k.lower()
        if "lik" in k:
            k = "likes_amount"
        if "twee" in k:
            k = "tweets_amount"
        if "followi" in k:
            k = "following_amount"
        if "followe" in k:
            k = "followers_amount"
        user[k] = v if v else 0

    logger.info("User Parsed {}".format(user["Id"]))
    logger.debug(repr(user.__dict__))
    return user
