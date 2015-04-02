# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacebookcrawlerItem(scrapy.Item):
	FirstName = scrapy.Field()
	LastName = scrapy.Field()
	PageUrl = scrapy.Field()
	Location = scrapy.Field()
	Phone = scrapy.Field()
	Email = scrapy.Field()
	
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
