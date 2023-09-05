from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader, GrantItem
from ..parsing import default_parser_xpath, get_dates


class SbpguSpider(CrawlSpider):
    name = "spbgu"
    un_name = 'Санкт-Петербургский государственный университет'
    allowed_domains = ["spbu.ru"]
    start_urls = ["https://spbu.ru/topics/108"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.card__header'), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        dates = response.xpath("string(//div[@class='event-details__date'])").get()
        new_item = get_dates(dates, new_item)
        new_item.add_xpath('conf_address', "string(//div[@class='event-details__place'])")

        for line in response.xpath("//div[@class='post']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()


class SbpguGrantSpider(CrawlSpider):
    name = "grant_spbgu"
    un_name = 'Санкт-Петербургский государственный университет'
    allowed_domains = ["spbu.ru"]
    start_urls = ["https://nauka.spbu.ru/nauchnye-granty-i-konkursy.html"]
    rules = (
        Rule(LinkExtractor(restrict_css='h3.catItemTitle', restrict_text='(?i)конкурс'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=GrantItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h2.itemTitle::text")
        for line in response.xpath("//div[@class='itemFullText']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
