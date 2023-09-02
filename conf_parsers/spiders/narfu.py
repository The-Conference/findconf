from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class NarfuSpider(CrawlSpider):
    name = "narfu"
    un_name = 'Северный (Арктический) федеральный университет имени М.В. Ломоносова'
    allowed_domains = ["narfu.ru"]
    start_urls = ["https://narfu.ru/science/nauchnye-meropriyatiya/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.events', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h5/text()")

        for line in response.xpath("//div[@class='events']//*[self::p or self::li or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        new_item.replace_xpath('description', "string(//div[@class='text_news'])")
        yield new_item.load_item()
