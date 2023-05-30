from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class NarfuSpider(CrawlSpider):
    name = "narfu"
    un_name = 'Северный (Арктический) федеральный университет имени М.В. Ломоносова'
    allowed_domains = ["narfu.ru"]
    start_urls = ["https://narfu.ru/science/nauchnye-meropriyatiya/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.events', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.url.split('=')[-1]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.xpath("//h5/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)

        conf_block = soup.find('div', class_='events')
        lines = conf_block.find_all(['p', 'li', 'h3'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
