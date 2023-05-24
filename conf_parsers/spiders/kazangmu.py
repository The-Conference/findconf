import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class KazangmuSpider(scrapy.Spider):
    name = "kazangmu"
    un_name = 'Казанский государственный медицинский университет'
    allowed_domains = ["kazangmu.ru"]
    start_urls = ["https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii",
                  "https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii?start=10",
                  "https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii?start=20"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_xpaths="//section[@id='content']//a", restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('/')[-1].split('-')[0]}")
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_name', conf_name)
        if dates := find_date_in_string(conf_name):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        conf_block = soup.find('article', class_='item')
        lines = conf_block.find('div', class_='content clearfix').find_all(['p', 'div'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()

