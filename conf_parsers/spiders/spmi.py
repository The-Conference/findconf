from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class SpmiSpider(CrawlSpider):
    name = "spmi"
    un_name = 'Санкт-Петербургский горный университет'
    allowed_domains = ["spmi.ru"]
    start_urls = ["http://nauka.spmi.ru/yesterday-today-tomorrow"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.konferencii a'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        header = response.xpath("string(//span[@class='title stroke'])").get()
        date = response.css("div.main-title div.wrapper > span.info").get()
        if not date:
            date = header.split('\n')[-1]
        new_item.add_value('conf_name', ''.join(header[:-1]))
        new_item = get_dates(date, new_item)

        for line in response.xpath("//div[@class='field__item']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)

        descr = response.xpath("string(//div[contains(@class, 'primary')][1])").get()
        new_item.replace_value('conf_desc', descr)
        addr = response.css("div#Contacts div.column:nth-child(2)").xpath("string(.)").get()
        new_item.replace_value('conf_address', addr)

        yield new_item.load_item()
