from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class PstuSpider(CrawlSpider):
    name = "pstu"
    un_name ='Пермский Национальный Исследовательский Политехнический Университет'
    allowed_domains = ["pstu.ru"]
    start_urls = ["https://pstu.ru/tag_news/?tag=14"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.news_item > a', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h1/text()")

        for line in response.css("div.news > div.text").xpath(".//*[self::p or self:: ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
