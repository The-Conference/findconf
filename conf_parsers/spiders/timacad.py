from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class TimacadSpider(CrawlSpider):
    name = 'timacad'
    un_name = 'Российский государственный аграрный университет - МСХА имени К.А. Тимирязева'
    allowed_domains = ['timacad.ru']
    start_urls = ['https://www.timacad.ru/science/konferentsii']
    rules = (
        Rule(
            LinkExtractor(restrict_css='a.announce-item', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', 'h1.news-inner__title::text')
        new_item.add_xpath('short_description', "string(//p[@class='news-inner__description'])")
        date = response.css('span.news-inner__date::text').get()
        new_item = get_dates(date, new_item)

        for line in response.xpath(
            "//div[@class='news-inner__content']/*[self::p or self::ul or self::ol]"
        ):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
