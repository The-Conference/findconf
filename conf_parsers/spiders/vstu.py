import datetime
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class VstuSpider(CrawlSpider):
    name = "vstu"
    un_name = 'Волгоградский государственный технический университет'
    allowed_domains = ["www.vstu.ru"]
    start_urls = ["https://www.vstu.ru/nauka/konferentsii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='dl.conf', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def start_requests(self):
        year = datetime.datetime.now().year
        yield scrapy.Request(self.start_urls.pop() + str(year))

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        new_item.add_css('conf_s_desc', "h1::text")
        date = response.xpath("string(//div[@class='content-wrapper']//p)").get()
        new_item = get_dates(date, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='content-wrapper').find('div', class_='unit-75')
        lines = conf_block.find_all(['td', 'li', 'p'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
