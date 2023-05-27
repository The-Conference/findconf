import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class MietSpider(scrapy.Spider):
    name = "miet"
    un_name = 'Национальный исследовательский университет «МИЭТ»'
    allowed_domains = ["miet.ru"]
    start_urls = ["https://miet.ru/"]

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        "DOWNLOADER_MIDDLEWARES": {
            'conf_parsers.middlewares.SeleniumMiddleware': 543,
        },
    }

    def parse(self, response, **kwargs):
        main_page = LinkExtractor(restrict_css='div.header-menu__toggable-item__list-item',
                                  restrict_text='Конференции и семинары')
        url = main_page.extract_links(response)[0].url
        yield scrapy.Request(url, callback=self.get_links)

    def get_links(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.site-sidebar__item-link',
                                       restrict_text='^((?!Архив).)*$')
        links = [i.url for i in link_extractor.extract_links(response)]
        links.append(response.url)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-1]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.xpath("//h2/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name else True)

        main_container = soup.find('div', class_='info-content')
        lines = main_container.find_all(['p'])
        for line in lines:
            new_item.add_value('conf_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)
        new_item.add_value('conf_s_desc', conf_name)
        yield new_item.load_item()
