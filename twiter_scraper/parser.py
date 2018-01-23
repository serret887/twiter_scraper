# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Selector
from scrapy.loader import ItemLoader
from twiter_scraper.items import Tweet, User


def parse_tweets(html_tweets):
    logger = logging.getLogger("Parser.Tweet")
    logger.debug("Parsing Tweet")
    tweet_list = Selector(text=html_tweets).xpath('//li[@data-item-id]')
    # //li in @id, stream-item-tweet)]'
    for t in tweet_list:
        logger.debug("Processing Tweets")
        item = Tweet()
        item["Id"] = t.xpath('.//@data-tweet-id').extract_first()
        logger.debug("Tweeter Id:%s" % item["Id"])
        item["user_id"] = t.xpath(
            './/span in @class,"username")]/b/text()').extract_first()
        logger.debug("User Id:%s" % item["user_id"])

        # TODO: convert to UTC
        date = t.xpath('.//span/@data-time').extract_first()
        item["created_date"] = datetime.fromtimestamp(
            int(date)).strftime('%Y-%m-%d %H:%M:%S')

        logger.debug("Tweet created_date:%s" % item["created_date"])

        item["permanent_link"] = t.xpath(
            './/@data-permalink-path').extract_first()

        logger.debug("URL: {}".format(item["created_date"]))

        # content extraction
        item["text"] = ' '.join(
            t.xpath('.//div in @class, "text")]//text()')
            .extract()).strip().replace('\n', '')
        # TODO fixing problems with URLs inside the text

        logger.debug("Tweet text: %s" % item["text"])
        stats = t.xpath(
            './/span in @class, "actionCount")]/span/text()').extract()
        logger.debug("Tweet Stats: {}".format(stats))
        # #TODO mayber use some contains here
        for stat in stats[:3]:
            v, k = stat.strip().split()
            logger.debug("Tweet Stats: {}:{}".format(k, v))
            if k in "repl":
                k = "replies_amount"
            if k in "lik":
                k = "likes_amount"
            if k in "retwe":
                k = "retweets_amount"
            item[k] = v if v else 0

        # get photo

        item["images"] = t.xpath(".//*/div/@data-image-url").extract()
        logger.debug("Tweet images: %s" % item["images"])
        item["cards"] = t.xpath('.//*/div/@data-card-url').extract()
        logger.debug("cards: {}".format(item["cards"]))
        yield item


def parse_users(response):
    import pdb
    pdb.set_trace()

    logger = logging.getLogger("Parser.User")
    logger.debug("Parsing User")
    json_response = json.loads(response.text)
    user = User()
    user["Id"] = json_response["user_id"]
    user["user_name"] = json_response["screen_name"]

    html = Selector(text=json_response["html"])

    user["name"] = html.xpath(
        './/a in @class, "fullname")]/text()').extract_first().strip()
    user["description"] = html.xpath(
        './/p in @class, "bio")]/text()').extract_first()

    stats = html.xpath(
        './/a in @class,"ProfileCardStats-statLink")]/@title').extract()

    for stat in stats[:3]:
        v, k = stat.strip().split()
        if k in "repl":
            k = "replies_amount"
        if k in "lik":
            k = "likes_amount"
        if k in "retwe":
            k = "retweets_amount"
        logger.debug("User Stats: {}:{}".format(k, v))
        user[k] = v if v else 0
    yield user
