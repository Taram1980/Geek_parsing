# Define your item pipelines hered
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.Instagram_followers_and_following

    def process_item(self, item, spider):
        collection = self.mongobase[item['status']]
        collection.update_one({'all_data': item['all_data']}, {'$set': item}, upsert=True)
        return item


class InstagramPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item
