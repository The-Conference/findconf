from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class TsuabSpider(CrawlSpider):
    name = "tsuab"
    un_name = 'Томский государственный архитектурно-строительный университет'
    allowed_domains = ["tsuab.ru"]
    start_urls = ["https://tsuab.ru/events/?SECTION_ID=264"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.events-list-item__content', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        conf_s_desc = response.xpath("string(//div[@class='detail__description']/p)").get()
        new_item.add_value('short_description', conf_s_desc)

        for line in response.xpath("//div[@class='detail__description textblock']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.meta.get('link_text'), new_item)

        yield new_item.load_item()
