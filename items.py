# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WhiskyadvocateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rating = scrapy.Field()
    brand = scrapy.Field()
    abv = scrapy.Field()
    style = scrapy.Field()
    price = scrapy.Field()
    review = scrapy.Field()
    reviewer = scrapy.Field()
