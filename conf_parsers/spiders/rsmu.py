import scrapy
from scrapy.spiders import CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class RsmuSpider(CrawlSpider):
    name = "rsmu"
    un_name = 'Российский национальный исследовательский медицинский университет имени Н.И. Пирогова'
    allowed_domains = ["rsmu.ru"]
    start_urls = ["https://rsmu.ru/events/"]

    def parse_start_url(self, response, **kwargs):
        for card in response.css("div.event-info"):
            text = card.xpath("string(.)").get()
            if 'конфер' in text.lower():
                link = card.xpath(".//a[contains(., 'Подробнее')]/@href").get()
                yield scrapy.Request(link, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//div[@class='event-name'])")

        for line in response.xpath("//div[@class='event-teaser']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        dates_str = response.xpath("string(//div[@class='event-date'])").get()
        new_item = get_dates(dates_str, new_item)
        yield new_item.load_item()
