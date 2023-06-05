from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


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

        new_item.add_value('conf_card_href', response.url)
        new_item.add_xpath('conf_name', "//h1/text()")
        conf_s_desc = response.xpath("string(//p/strong)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='news full_news')
        lines = conf_block.find('div', class_='text').find_all(['p', 'ul'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
