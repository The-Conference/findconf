from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class RosnouSpider(CrawlSpider):
    name = "rosnou"
    un_name = 'Российский новый университет'
    allowed_domains = ["rosnou.ru"]
    start_urls = ["https://rosnou.ru/nauka/conferences/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.article-card'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.css("div.content-header__title-inner::text").get()
        conf_s_desc = ''
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='stage -gap-grid-inner_y_medium')
        lines = conf_block.find_all(['p', 'li', 'ol'])
        for line in lines:
            if not conf_s_desc:
                conf_s_desc = line
            new_item = default_parser_bs(line, new_item)
        new_item.add_value('conf_s_desc', conf_name)
        yield new_item.load_item()
