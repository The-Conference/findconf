from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class BashgmuSpider(CrawlSpider):
    name = "bashgmu"
    un_name = 'Башкирский государственный медицинский университет'
    allowed_domains = ["bashgmu.ru"]
    start_urls = ["https://bashgmu.ru/science_and_innovation/konferentsii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='p.grants-item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("string(//h3)").get()
        new_item.add_value('title', conf_name)
        new_item.add_value('source_href', response.url)
        new_item.add_value('online', True if 'онлайн' in conf_name.lower() or
                                             'он-лайн' in conf_name.lower() else False)

        for line in response.xpath("//div[@class='grants-detail']/*[self::p or self::h3]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
