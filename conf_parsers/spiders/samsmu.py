import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class SamsmuSpider(scrapy.Spider):
    name = "samsmu"
    un_name = 'Самарский государственный медицинский университет'
    allowed_domains = ["samsmu.ru"]
    start_urls = ["https://samsmu.ru/events"]
    headers = {
        "cookie": "psy=x.yz; psy=x.yz",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "psy=x.yz; PHPSESSID=qasch7ite3gg9fkf10hs0e6jfm",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls.pop(), headers=self.headers, callback=self.parse_links)

    def parse_links(self, response):
        link_extractor = LinkExtractor(restrict_css='a.link.block.w-full.h-250', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, meta={'data': link.text},
                                 headers=self.headers, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_xpath('conf_name', "string(//h1)")
        conf_s_desc = response.xpath("string(//p[not(@class)])").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('section', class_='pb-40 text_section').find('div', class_='row')
        lines = conf_block.find_all('div', class_='col-xl-12 col-lg-12')[-1].find_all(['p'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            if dates := find_date_in_string(response.meta.get('data')):
                new_item.add_value('conf_date_begin', dates[0])
                new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
        yield new_item.load_item()
