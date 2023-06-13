from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class BmstuSpider(CrawlSpider):
    name = "bmstu"
    un_name = 'Московский государственный технический университет им. Н.Э. Баумана'
    allowed_domains = ["bmstu.ru"]
    start_urls = ["https://bmstu.ru/events?category=konferencii-i-forumy&isActual=1"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.Card_default'), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_xpath('conf_name', "string(//h5)")
        new_item.add_value('conf_card_href', response.url)

        for line in response.xpath("//div[@class='EventsMainContent__content']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
