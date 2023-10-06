import scrapy
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class SamsmuSpider(scrapy.Spider):
    name = 'samsmu'
    un_name = 'Самарский государственный медицинский университет'
    allowed_domains = ['samsmu.ru']
    start_urls = ['https://samsmu.ru/events']
    headers = {
        'cookie': 'psy=x.yz; psy=x.yz',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'psy=x.yz; PHPSESSID=qasch7ite3gg9fkf10hs0e6jfm',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls.pop(), headers=self.headers, callback=self.parse_links
        )

    def parse_links(self, response):
        link_extractor = LinkExtractor(
            restrict_css='a.link.block.w-full.h-250', restrict_text='онференц'
        )
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(
                link.url, meta={'data': link.text}, headers=self.headers, callback=self.parse_items
            )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', 'string(//h1)')

        for line in response.xpath("//div[@class='col-xl-12 col-lg-12']/*[self::p]"):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.meta.get('data'), new_item)
        yield new_item.load_item()
