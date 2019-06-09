# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class DBItem(Item):
    name = Field()
    chapter_title = Field()
    page_num = Field()
    image_url = Field()