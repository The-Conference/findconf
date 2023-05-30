import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class PetrsuSpider(scrapy.Spider):
    name = "petrsu"
    un_name = 'Петрозаводский государственный университет'
    allowed_domains = ["conf.petrsu.ru"]
    start_urls = ["https://conf.petrsu.ru/index.php"]

    def parse(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.css('div#conf_name::text').get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_id', f"{self.name}_{''.join(conf_name.split())}")
        new_item.add_value('conf_card_href', response.url)
        conf_s_desc = response.css('p::text').get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)

        dates = response.xpath("string(//div[@id='conf_name'])").get()
        if dates := find_date_in_string(dates):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', id='conf_desc')
        lines = conf_block.find_all(['div', 'p', 'table'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()


class PetrsuPagesSpider(CrawlSpider):
    name = "petrsu_pages"
    un_name = 'Петрозаводский государственный университет'
    allowed_domains = ["petrsu.ru"]
    start_urls = ["https://petrsu.ru/page/education/school/project/konferentsii-i-konkursy"]
    rules = (
        Rule(LinkExtractor(restrict_css='h4', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='ul.pagination > li.next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_id', f"{self.name}_{''.join(conf_name.split())}")
        new_item.add_value('conf_card_href', response.url)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='col-sm-8 col-xs-12 page-content')
        lines = conf_block.find_all(['p', 'ul'])
        conf_s_desc = ''
        for line in lines:
            if not conf_s_desc:
                new_item.add_value('conf_s_desc', line.text)
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
