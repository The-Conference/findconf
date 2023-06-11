from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class SbpguSpider(CrawlSpider):
    name = "sbpgu"
    un_name = 'Санкт-Петербургский государственный университет'
    allowed_domains = ["spbu.ru"]
    start_urls = ["https://spbu.ru/topics/108"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.card__header'), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        dates = response.xpath("string(//div[@class='event-details__date'])").get()
        new_item = get_dates(dates, new_item)
        new_item.add_xpath('conf_address', "string(//div[@class='event-details__place'])")

        for line in response.xpath("//div[@class='post']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
