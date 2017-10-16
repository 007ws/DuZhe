# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuzheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    Content = scrapy.Field()
    link = scrapy.Field()

    journal = scrapy.Field()
    topic = scrapy.Field()
