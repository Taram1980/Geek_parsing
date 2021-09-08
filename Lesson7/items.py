# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def clean_price(value):
    try:
        value = float(value.replace('\n', '').replace(' ', ''))
    except ValueError:
        pass
    return value

def clean_details(dict_):
  if type(dict_) == dict:
    for k, v in dict_.items():
      dict_[k] = v.replace('\n', '').replace(' ', '')
      try:
        dict_[k] = float(dict_[k])
      except TypeError and ValueError:
        pass
  return dict_


class LeruaparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    details = scrapy.Field(input_processor=MapCompose(clean_details), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())
    _id = scrapy.Field()

