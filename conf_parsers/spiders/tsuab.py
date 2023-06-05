import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class TsuabSpider(scrapy.Spider):
    name = "tsuab"
    un_name = 'Томский государственный архитектурно-строительный университет'
    allowed_domains = ["tsuab.ru"]
    start_urls = ["https://tsuab.ru/events/?SECTION_ID=264"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.events-list-item__content', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, meta={'data': link.text}, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        conf_s_desc = response.xpath("string(//div[@class='detail__description']/p)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='detail__description textblock')
        lines = conf_block.find_all(['p', 'ul', 'ol'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.meta.get('data'), new_item)

        yield new_item.load_item()
