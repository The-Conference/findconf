import datetime
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class VstuSpider(CrawlSpider):
    name = "vstu"
    un_name = 'Волгоградский государственный технический университет'
    allowed_domains = ["www.vstu.ru"]
    start_urls = ["https://www.vstu.ru/nauka/konferentsii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='dl.conf', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def start_requests(self):
        year = datetime.datetime.now().year
        yield scrapy.Request(self.start_urls.pop() + str(year))

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        date = response.xpath("string(//div[@class='content-wrapper']//p)").get()
        new_item = get_dates(date, new_item)

        for line in response.xpath("//div[@class='unit-75']//*[self::p or self::td or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
