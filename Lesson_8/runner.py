from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_8.instaparser.spiders.follow_parser import FollowSpider
from Lesson_8.instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(FollowSpider)

    process.start()
