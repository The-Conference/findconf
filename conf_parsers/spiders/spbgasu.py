import scrapy
from bs4 import BeautifulSoup

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string, parse_vague_dates


class SpbgasuSpider(scrapy.Spider):
    name = "spbgasu"
    un_name = 'Санкт-Петербургский государственный архитектурно-строительный университет'
    allowed_domains = ["spbgasu.ru"]
    start_urls = ["https://www.spbgasu.ru/science/konferentsii-i-seminary/"]

    def parse(self, response, **kwargs):
        for row in response.css('tr'):
            cells = row.css('td')
            if len(cells) > 1:
                href = cells[1].css('a::attr(href)').get()
                title = cells[1].xpath("string(.)").get()
                contacts = cells[-1].xpath("string(.)").get()
                if href and 'онференц' in title.lower():
                    yield scrapy.Request(response.urljoin(href), callback=self.parse_items,
                                         meta={'contacts': contacts})

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_xpath('conf_name', "string(//h1[@class='page-head__title'])")
        conf_s_desc = response.xpath("string(//p[contains(@class, 'page-head__subtitle')])").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        dates = find_date_in_string(conf_s_desc)
        if not dates:
            dates = parse_vague_dates(conf_s_desc)
        if dates:
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('main')
        lines = conf_block.find_all(['p', 'ul', 'h2', 'section'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        new_item.replace_value('contacts', response.meta.get('contacts'))
        yield new_item.load_item()
