from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class RzgmuSpider(CrawlSpider):
    name = "rzgmu"
    un_name = 'Рязанский государственный медицинский университет имени академика И.П. Павлова'
    allowed_domains = ["rzgmu.ru"]
    start_urls = ["https://rzgmu.ru/actions/"]
    rules = (
        Rule(LinkExtractor(restrict_css='article > a.title', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.year.current')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.css("h1::text").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        conf_s_desc = response.xpath("string(//div[@class='text']/p)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('main', id='internal')
        lines = conf_block.find('div', class_='text').find_all(['p', 'ul'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()

