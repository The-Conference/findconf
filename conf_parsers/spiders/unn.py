from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader, GrantItem
from ..parsing import default_parser_xpath, get_dates


class UnnSpider(CrawlSpider):
    name = "unn"
    un_name = 'Нижегородский государственный университет им. Н.И. Лобачевского'
    allowed_domains = ["unn.ru"]
    start_urls = ["http://nauka.unn.ru/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.events__item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1)")

        for line in response.xpath("//div[@class='content-style']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('description'), new_item)

        yield new_item.load_item()


class UnnGrantSpider(CrawlSpider):
    name = "grant_unn"
    un_name = 'Нижегородский государственный университет им. Н.И. Лобачевского'
    allowed_domains = ["unn.ru"]
    start_urls = ["http://nauka.unn.ru/grants/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.active a.grants__item-more'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=GrantItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1)")

        for line in response.xpath("//div[@class='content-style']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)

        if reg := new_item.get_collected_values('reg_date_end'):
            new_item.replace_value('reg_date_end', reg[-1])
        yield new_item.load_item()
