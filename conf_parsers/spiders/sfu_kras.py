import scrapy
from bs4 import BeautifulSoup
import html

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class SfuKrasSpider(scrapy.Spider):
    name = "sfu-kras"
    un_name = 'Сибирский федеральный университет'
    allowed_domains = ["conf.sfu-kras.ru"]
    start_urls = ["https://conf.sfu-kras.ru/"]

    def parse(self, response, **kwargs):
        for link in response.css('div.listItem'):
            href = link.css('a::attr(href)').get()
            if 'онференц' in link.xpath('string(.)').get():
                yield scrapy.Request(response.urljoin(href), callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_xpath('conf_name', "string(//h2)")
        new_item.add_xpath('conf_s_desc', "string(//h4)")

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='confs-container')
        lines = conf_block.find_all('div', class_='row')
        for line in lines:
            new_item = default_parser_bs(line, new_item)
            if 'сайт' in line.text.lower():
                new_item.add_value('conf_href', line.find('a').get('href'))
            if 'mail' in line.text.lower():
                encoded = str(line.find('script').text)
                if decoded := self.decode_email(encoded):
                    new_item.add_value('contacts', decoded)
        yield new_item.load_item()

    @staticmethod
    def decode_email(encoded: str) -> str:
        prep = encoded.split('"')[1::2][0].replace("'+'", "")
        decode = html.unescape(prep)
        decode = decode.replace('mailto:', '')
        return decode
