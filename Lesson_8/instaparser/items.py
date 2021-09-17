# Define here the models for your scraped itemsd
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:

    id = scrapy.Field()
    name = scrapy.Field()
    photo = scrapy.Field()
    status = scrapy.Field()
    user_parse = scrapy.Field()
    all_data = scrapy.Field()
