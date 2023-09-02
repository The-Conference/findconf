from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class SechenovSpider(CrawlSpider):
    name = "sechenov"
    un_name = 'Первый МГМУ им. И.М. Сеченова Минздрава России (Сеченовский Университет)'
    allowed_domains = ["www.sechenov.ru"]
    start_urls = ["https://www.sechenov.ru/pressroom/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event-descr-wrap', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//div[@class='news-header'])")

        for line in response.xpath("//div[@class='event-detail-txt']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
