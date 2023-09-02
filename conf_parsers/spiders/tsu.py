import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class TsuSpider(scrapy.Spider):
    name = "tsu"
    un_name = 'Национальный исследовательский Томский государственный университет'
    allowed_domains = ["tsu.ru"]
    start_urls = ["https://news.tsu.ru/calendar-of-events/rss.php"]

    def parse(self, response, **kwargs):
        for item in response.xpath('//channel/item'):
            title = item.xpath('title//text()').get()
            link = item.xpath('link//text()').get()
            if 'онференц' in title:
                yield scrapy.Request(link, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")

        for line in response.xpath("//div[@class='text-content']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.xpath("string(//div[@class='address'])").get(), new_item)

        yield new_item.load_item()
