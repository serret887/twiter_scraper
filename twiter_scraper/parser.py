# -*- coding: utf-8 -*-
import json
from datetime import datetime

from scrapy import Selector
from scrapy.loader import ItemLoader

from twiter_scraper.items import Tweet, User


def parse_tweets(html_tweets, logger):
    logger.debug("Parsing Tweet")
    tweet_list = Selector(text=html_tweets).xpath('//li[@data-item-id]')
    # //li[contains(@id, stream-item-tweet)]'
    for t in tweet_list:
        logger.debug("Processing Tweets")
        item = Tweet()
        item["Id"] = t.xpath('.//@data-tweet-id').extract_first()
        logger.debug("Tweeter Id:%s" % item["Id"])
        item["user_id"] = t.xpath(
            './/span[contains(@class,"username")]/b/text()').extract_first()
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
            t.xpath('.//div[contains(@class, "text")]//text()')
            .extract()).strip()
        # TODO fixing problems with URLs inside the text

        logger.debug("Tweet text: %s" % item["text"])
        stats = t.xpath(
            './/span[contains(@class, "actionCount")]/span/text()').extract()
        logger.debug("Tweet Stats: {}".format(stats))
        # #TODO mayber use some contains here
        for stat in stats:
            v, k = stat.strip().split()
            logger.debug("{}:{}".format(k, v))
            item[k] = v if v else 0

        # get photo

        item["images"] = t.xpath(".//*/div/@data-image-url").extract()
        logger.debug("Tweet images: %s" % item["images"])
        item["cards"] = t.xpath('.//*/div/@data-card-url').extract()
        logger.debug("cards: {}".format(item["cards"]))
        yield item


def parse_users(response, logger):
    logger.debug("Parsing User")
    json_response = json.loads(response.text)
    user = User()
    user["Id"] = json_response["user_id"]
    user["user_name"] = json_response["screen_name"]

    html = Selector(text=json_response["html"])

    user["name"] = html.xpath(
        './/a[contains(@class, "fullname")]/text()').extract_first().strip()
    user["description"] = html.xpath(
        './/p[contains(@class, "bio")]/text()').extract_first()

    stats = html.xpath('.//')
