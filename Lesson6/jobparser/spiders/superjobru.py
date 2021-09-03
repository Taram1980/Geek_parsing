import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vakansii/buhgalter.html']

    def parse(self, response: HtmlResponse):
        # print()
        urls = response.xpath("//div[contains(@class,'f-test-vacancy-item')]//a[contains(@href, 'vakansii')]/@href").getall()
        next_page = response.xpath("//a[contains(@class,'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//h1/following-sibling::span//text()").getall()
        vac_url = response.url
        item = JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)
        yield item