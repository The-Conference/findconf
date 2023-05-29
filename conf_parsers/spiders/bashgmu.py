from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class BashgmuSpider(CrawlSpider):
    name = "bashgmu"
    un_name = 'Башкирский государственный медицинский университет'
    allowed_domains = ["bashgmu.ru"]
    start_urls = ["https://bashgmu.ru/science_and_innovation/konferentsii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='p.grants-item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        soup = BeautifulSoup(response.text, 'lxml')
        main_containers = soup.find('div', class_='grants-detail')

        conf_name = response.xpath("//h3/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_value('online', True if 'онлайн' in conf_name.lower() or
                                             'он-лайн' in conf_name.lower() else False)

        for line in main_containers.find_all(['h3', 'p']):
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
