import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class ToguSpider(scrapy.Spider):
    name = "togu"
    un_name = 'Тихоокеанский государственный университет'
    allowed_domains = ["pnu.edu.ru"]
    start_urls = ["https://pnu.edu.ru/ru/news/channels/events/conferences/"]
    custom_settings = {
        'COOKIES_ENABLED': True,
    }

    def parse(self, response, **kwargs):
        for card in response.css("div.col-with-img"):
            if 'онференц' in card.xpath("string(.)").get().lower():
                href = card.xpath("./h2/a/@href").get()
                yield scrapy.Request(href, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        new_item.add_xpath('short_description', "string(//div[@class='news_abstract'])")

        for line in response.xpath("//div[@class='text-plugin']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
