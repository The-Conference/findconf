from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class KbsuSpider(CrawlSpider):
    name = "kbsu"
    un_name = 'Кабардино-Балкарский государственный университет им. Х. М. Бербекова'
    allowed_domains = ["kbsu.ru"]
    start_urls = ["https://kbsu.ru/nauchnye-konferencii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='td > a', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item = get_dates(conf_name, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        main_container = soup.find('div', class_='single__content content')
        lines = main_container.find_all(['p', 'ul', 'ol'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
