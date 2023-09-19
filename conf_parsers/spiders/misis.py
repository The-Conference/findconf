from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from dateparser import parse

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MisisSpider(CrawlSpider):
    name = "misis"
    un_name = 'Университет науки и технологий МИСИС'
    allowed_domains = ["misis.ru"]
    start_urls = ["https://misis.ru/university/events/conference/"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.calend-event', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h1/text()")
        conf_date_begin = response.xpath("//canvas/@data-begin-datetime").get()
        conf_date_begin = parse(conf_date_begin, settings={'DATE_ORDER': 'YMD'}).date()
        new_item.add_value('conf_date_begin', conf_date_begin)
        conf_date_end = response.xpath("//canvas/@data-end-datetime").get()
        conf_date_end = parse(conf_date_end, settings={'DATE_ORDER': 'YMD'}).date()
        if conf_date_end != conf_date_begin:
            new_item.add_value('conf_date_end', conf_date_end)
        new_item.add_css('conf_address', "div.article-meta-place::text")

        for line in response.xpath("//div[@class='article__inner']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()

