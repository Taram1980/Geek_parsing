import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpiderSpider(scrapy.Spider):
    name = 'leroymerlin_spider'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse, **kwargs):
        urls = response.xpath("//a[@data-qa='product-name']")
        next_page_button = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.parse_goods)


    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value("link", response.url)

        details_names = response.xpath("//dt/text()").getall()
        details_param = response.xpath("//dd/text()").getall()
        details = dict(zip(details_names, details_param))
        loader.add_value('details', details)

        yield loader.load_item()