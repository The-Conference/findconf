import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class MgppuSpider(scrapy.Spider):
    name = "mgppu"
    un_name = 'Московский государственный психолого-педагогический университет'
    allowed_domains = ["mgppu.ru"]
    start_urls = ["https://mgppu.ru/events?searchStr=&eventtype_conference=y"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.new-link', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, meta={'desc': link.text}, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        dates = response.xpath("//time/text()").get()
        if dates := find_date_in_string(dates):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('/')[-1]}")
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name else True)

        conf_block = soup.find('div', class_='page container').find('div', class_='col-sm-12')
        lines = conf_block.find_all(['p', 'ul', 'ol'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
