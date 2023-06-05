from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class KazangmuSpider(CrawlSpider):
    name = "kazangmu"
    un_name = 'Казанский государственный медицинский университет'
    allowed_domains = ["kazangmu.ru"]
    start_urls = ["https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii",
                  "https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii?start=10",
                  "https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii?start=20"]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//section[@id='content']//a", restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item = get_dates(conf_name, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('article', class_='item')
        lines = conf_block.find('div', class_='content clearfix').find_all(['p', 'div'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
