from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class DonstuSpider(CrawlSpider):
    name = "donstu"
    un_name = 'Донской государственный технический университет'
    allowed_domains = ["donstu.ru"]
    start_urls = ["https://donstu.ru/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event-box', allow='konfer'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("//div[@class='title']/text()").get()
        new_item.add_value('conf_name', conf_name)
        conf_s_desc = response.xpath("//div[@class='desc']/text()").get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        new_item.add_value('conf_card_href', response.url)
        conf_date_begin = response.xpath("string(//div[@class='event-date'])").get()
        new_item = get_dates(conf_date_begin, new_item)
        conf_address = response.xpath("string(//div[@class='event-location'])").get()
        new_item.add_value('conf_address', conf_address)

        for line in response.xpath("//div[@class='text-block']/*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)

        online = True if 'онлайн' in conf_address.lower() else False
        new_item.add_value('online', online)
        new_item.add_value('offline', not online)

        yield new_item.load_item()
