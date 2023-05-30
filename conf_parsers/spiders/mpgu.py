from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class MpguSpider(CrawlSpider):
    name = "mpgu"
    un_name = 'Московский педагогический государственный университет'
    allowed_domains = ["mpgu.su"]
    start_urls = ["http://mpgu.su/category/anonsyi"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.media-body', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='ul.pagination > li > a', restrict_text='>>')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        dates = response.xpath("string(//h3)").get()
        if dates := find_date_in_string(dates):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        conf_block = soup.find('div', class_='content')
        lines = conf_block.find_all(['p', 'ul', 'ol', 'h6'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
