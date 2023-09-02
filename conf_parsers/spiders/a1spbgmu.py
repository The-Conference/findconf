from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class A1spbgmuSpider(CrawlSpider):
    name = "1spbgmu"
    un_name = 'Первый Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова'
    allowed_domains = ["www.1spbgmu.ru"]
    start_urls = ["https://www.1spbgmu.ru/nauka/konferentsii"]
    rules = (
        Rule(LinkExtractor(restrict_css='td.list-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("string(//div[@class='page-header'])").get()
        new_item.add_value('title', conf_name)
        new_item.add_value('source_href', response.url)
        new_item = get_dates(conf_name, new_item)

        for line in response.xpath("//div[@itemprop='articleBody']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
