import scrapy
from bs4 import BeautifulSoup

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class UniDubnaSpider(scrapy.Spider):
    name = "uni_dubna"
    un_name = 'Государственный университет "Дубна"'
    allowed_domains = ["uni-dubna.ru"]
    start_urls = ["https://conf.uni-dubna.ru/Home/Conferences"]

    def parse(self, response, **kwargs):
        for conf in response.css('div.card-body'):
            link = conf.css('a::attr(href)').get()
            date = find_date_in_string(conf.css('h5').get())
            if date[0] >= self.settings.get('FILTER_DATE'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1.title_one::text")
        conf_s_desc = response.xpath("string(//h5[@class='description info1'])").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        dates_select = response.xpath("string(//h4[@class='hero-text-small'])").get()
        if dates := find_date_in_string(dates_select):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='main main-raised').find('div', class_='container')
        lines = conf_block.find_all(['h2', 'h3', 'h5', 'p'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
