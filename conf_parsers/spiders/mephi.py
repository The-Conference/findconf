from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MifiSpider(CrawlSpider):
    name = "mephi"
    un_name = 'Национальный исследовательский ядерный университет «МИФИ»'
    allowed_domains = ["mephi.ru"]
    start_urls = ["https://mephi.ru/press/announcements"]
    rules = (
        Rule(LinkExtractor(restrict_css='span.field-content', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.pager-next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h1/text()")

        for line in response.xpath("//div[@class='field-items']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
