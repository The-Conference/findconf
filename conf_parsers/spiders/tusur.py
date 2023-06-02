from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class TusurSpider(CrawlSpider):
    name = "tusur"
    un_name = 'Томский государственный университет систем управления и радиоэлектроники'
    allowed_domains = ["tusur.ru"]
    start_urls = ["https://tusur.ru/ru/novosti-i-meropriyatiya/anonsy-meropriyatiy"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.event-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='span.next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        conf_s_desc = response.xpath("string(//div[@class='annotation-text'])").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='content index')
        lines = conf_block.find('div', class_='news-item').find_all(['p', 'li'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
