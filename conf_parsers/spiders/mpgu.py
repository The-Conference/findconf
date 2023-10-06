from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class MpguSpider(CrawlSpider):
    name = 'mpgu'
    un_name = 'Московский педагогический государственный университет'
    allowed_domains = ['mpgu.su']
    start_urls = ['http://mpgu.su/category/anonsyi']
    rules = (
        Rule(
            LinkExtractor(restrict_css='div.media-body', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
        Rule(LinkExtractor(restrict_css='ul.pagination > li > a', restrict_text='>>')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', '//h1/text()')
        new_item = get_dates(response.xpath('string(//h3)').get(), new_item)

        for line in response.xpath("//div[@class='content']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
