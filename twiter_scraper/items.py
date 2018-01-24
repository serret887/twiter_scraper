# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Tweet(Item):
    Id = Field()  # tweet id
    permanent_link = Field()  # tweet url
    created_date = Field()  # tweet posted time UTC
    text = Field()  # text content
    user_id = Field()  # user id
    user_name = Field()  # user name

    retweets_amount = Field()  # No of retweet
    likes_amount = Field()  # No of favorite
    replies_amount = Field()  # No of reply

    images = Field()  # a list of image urls
    cards = Field()  # a list of cards


class User(Item):
    Id = Field()  # user id
    user_name = Field()  # user name
    description = Field()  # description of the person
    avatar = Field()  # avatar url
    name = Field()  # name of the person

    tweets_amount = Field()
    following_amount = Field()
    followers_amount = Field()
    likes_amount = Field()
