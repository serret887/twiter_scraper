# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Tweet(Item):
    iD = Field()  # tweet id
    url = Field()  # tweet url
    created_date = Field()  # post time
    text = Field()  # text content
    user_id = Field()  # user id
    # TODO: check that i can search users by userId
    usernameTweet = Field()  # username of tweet

    retweet_amount = Field()  # nbr of retweet
    like_amount = Field()  # nbr of favorite
    reply_amount = Field()  # nbr of reply

    is_reply = Field()  # boolean if the tweet is a reply or not
    is_retweet = Field(
    )  # boolean if the tweet is just a retweet of another tweet

    has_image = Field()  # True/False, whether a tweet contains images
    images = Field()  # a list of image urls, empty if none

    has_video = Field()  # True/False, whether a tweet contains videos
    videos = Field()  # a list of video urls

    has_media = Field(
    )  # True/False, whether a tweet contains media (e.g. summary)
    medias = Field()  # a list of media


class User(Item):
    ID = Field()  # user id
    name = Field()  # user name
    screen_name = Field()  # user screen name
    avatar = Field()  # avator url

    tweets_amount = Field()
    following_amount = Field()
    follower_amount = Field()
    like_amount = Field()
