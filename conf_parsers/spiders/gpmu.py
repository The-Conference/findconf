import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class GpmuSpider(scrapy.Spider):
    name = "gpmu"
    un_name = 'Санкт-Петербургский государственный педиатрический медицинский университет'
    allowed_domains = ["gpmu.org"]
    start_urls = ["https://gpmu.org/science/conference/"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='div.catinfo_item', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.request.url}")
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("string(//h1)").get()
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_name', conf_name)
        table_date = response.xpath("string(//div[@id='content']//td)").get()
        if dates := find_date_in_string(table_date):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        conf_block = soup.find('div', id='content')
        lines = conf_block.find_all(['p', 'ul', 'span', 'div'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
