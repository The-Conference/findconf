import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class KurskmedSpider(scrapy.Spider):
    name = "kurskmed"
    un_name = 'Курский государственный медицинский университет'
    allowed_domains = ["kurskmed.com"]
    start_urls = ["https://kurskmed.com/department/KSMU_announcements_events/news"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='div.news_list', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, meta={'desc': link.text}, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('conf_name', "string(//div[@class='detail_title']/div[@class='detail_title'])")
        new_item.add_value('conf_s_desc', response.meta.get('desc'))

        soup = BeautifulSoup(response.text, 'lxml')
        main_block = soup.find('div', class_='detail_news clearfix')
        lines = main_block.find('div', class_='text_news').find_all()

        for line in lines:
            new_item = default_parser_bs(line, new_item)
            if 'гибридн' in line.text.lower():
                new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else None)
                new_item.add_value('online', True)
                new_item.add_value('conf_address', line.text)
                new_item.add_value('offline', True)

        yield new_item.load_item()
