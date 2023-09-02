from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
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
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1)")

        for line in response.xpath("//div[@class='content-style']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('description'), new_item)
        yield new_item.load_item()
