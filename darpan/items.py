# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DarpanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    cause_area=scrapy.Field()
    address=scrapy.Field()
    city=scrapy.Field()
    state=scrapy.Field()
    phone=scrapy.Field()
    email=scrapy.Field()
    website=scrapy.Field()
    
