import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class AsouMoSpider(scrapy.Spider):
    name = "asou_mo"
    un_name = 'Академия социального управления'
    allowed_domains = ["asou-mo.ru"]
    start_urls = [
        "https://asou-mo.ru/events/announce/",
        # "https://asou-mo.ru/events/archive"
    ]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.hentry', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find(
            'section', class_='one-news one-news--event container container--bordered_overflow hentry').find(
            'div', class_='container__inner')

        conf_name = conf_block.find('h1', class_='entry-title').text
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_name', conf_name)
        description = conf_block.find(
            'div', class_='one-news__intro-description').find('p', class_='entry-content')
        new_item.add_value('conf_s_desc', description.text)
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('=')[-1]}")
        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_value('org_name', conf_block.find(
            'a', class_='one-news__institute-link author').get_text(separator=' '))
        new_item.add_xpath('conf_address', "//div[contains(@class, 'tabs__place-info--loc')]//p[2]/text()")
        new_item.add_xpath('contacts', "//div[contains(@class, 'tabs__place-info--phone')]//p[2]/text()")
        new_item.add_css('reg_href', 'a.button--register::attr(href)')

        lines = conf_block.find(
            'div', class_='one-news__purposes container container--news-one common-text').find_all(
            ['p', 'ul', 'h3'])
        lines.extend(description)
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()