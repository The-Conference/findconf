from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class MgppuSpider(CrawlSpider):
    name = "mgppu"
    un_name = 'Московский государственный психолого-педагогический университет'
    allowed_domains = ["mgppu.ru"]
    start_urls = ["https://mgppu.ru/events?searchStr=&eventtype_conference=y"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.new-link', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)
        dates = response.xpath("//time/text()").get()
        new_item = get_dates(dates, new_item)
        new_item.add_value('source_href', response.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('title', conf_name)

        for line in response.xpath("//article/*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
