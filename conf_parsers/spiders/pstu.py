from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class PstuSpider(CrawlSpider):
    name = "pstu"
    un_name ='Пермский Национальный Исследовательский Политехнический Университет'
    allowed_domains = ["pstu.ru"]
    start_urls = ["https://pstu.ru/tag_news/?tag=14"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.news_item > a', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.xpath("//h1/text()").get()
        conf_s_desc = response.xpath("string(//p/strong)").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower()
                                             or 'международн' in conf_s_desc.lower() else True)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='news full_news')
        lines = conf_block.find('div', class_='text').find_all(['p', 'ul'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            if dates := find_date_in_string(conf_s_desc):
                new_item.add_value('conf_date_begin', dates[0])
                new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
        yield new_item.load_item()
