from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class SfeduSpider(CrawlSpider):
    name = 'sfedu'
    un_name = 'Южный федеральный университет'
    allowed_domains = ['sfedu.ru']
    start_urls = ['https://sfedu.ru/press-center/news/64233']
    current_year = str(datetime.now().year)
    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=f"//div[@class='content']//p[preceding::*[1][contains(.//text(), {current_year})]]//a",
                restrict_text='онференц',
            ),
            callback='parse_items',
            follow=False,
        ),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h3[@id='tit1'])")
        new_item.add_xpath('short_description', "string(//span[@class='short_description'])")

        for line in response.xpath("//div[@class='content']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
