from urllib.parse import urlencode
import scrapy
from bs4 import BeautifulSoup

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class PimunnSpider(scrapy.Spider):
    name = "pimunn"
    un_name = 'Приволжский исследовательский медицинский университет Министерства здравоохранения Российской Федерации'
    allowed_domains = ["feeds.tildacdn.com",
                       "project747694.tilda.ws"]

    def start_requests(self):
        feed = "https://feeds.tildacdn.com/api/getfeed/?"
        params = {
            'feeduid': '5da0b30957567621136849-830127464577',
            'recid': '134097321',
            'c': '1676878449022',
            'size': '10',
            'slice': '1',
            'sort[date]': 'desc',
            'filters[date]': '',
            'getparts': 'true',
        }
        yield scrapy.Request(feed + urlencode(params), callback=self.parse_links)

    def parse_links(self, response):
        for i in response.json()['posts']:
            yield scrapy.Request(i['url'], meta=i, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_value('conf_name', response.meta.get('title'))
        new_item.add_value('conf_s_desc', response.meta.get('descr'))

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='t-redactor__text')
        new_item = default_parser_bs(conf_block, new_item)
        yield new_item.load_item()