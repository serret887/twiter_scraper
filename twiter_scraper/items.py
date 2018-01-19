# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import json

from scrapy import Field, Item


class Tweet(Item):
    Id = Field()  # tweet id
    url = Field()  # tweet url
    created_date = Field()  # tweet posted time UTC
    text = Field()  # text content
    user_id = Field()  # user id

    retweets = Field()  # No of retweet
    likes = Field()  # No of favorite
    replies = Field()  # No of reply

    images = Field()  # a list of image urls
    cards = Field()  # a list of cards

    def __str__(self):
        return json.dumps(self)


class User(Item):
    Id = Field()  # user id
    name = Field()  # user name
    screen_name = Field()  # user screen name
    avatar = Field()  # avatar url

    tweets_amount = Field()
    following_amount = Field()
    follower_amount = Field()
    like_amount = Field()

    def __str__(self):
        return json.dumps(self)
