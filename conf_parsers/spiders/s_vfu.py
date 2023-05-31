from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class SVfuSpider(CrawlSpider):
    name = "s-vfu"
    un_name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
    allowed_domains = ["www.s-vfu.ru"]
    start_urls = ["https://www.s-vfu.ru/universitet/nauka/sciconf/"]
    rules = (
        Rule(LinkExtractor(restrict_css='h3', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.bx-pag-next')),
    )
    custom_settings = {
        "DEPTH_LIMIT": 3
    }

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "div.px-4 > h2::text")
        conf_s_desc = response.xpath("string(//div[@class='px-4']/div/p)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='px-4')
        lines = conf_block.find('div').find_all(['p', 'div', 'h1'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            if dates := find_date_in_string(response.xpath("string(//div[@class='px-4']/div)").get()):
                new_item.add_value('conf_date_begin', dates[0])
                new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
        yield new_item.load_item()
