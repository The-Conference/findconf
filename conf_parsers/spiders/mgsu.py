import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class MgsuSpider(scrapy.Spider):
    name = "mgsu"
    un_name = 'Московский городской педагогический университет'
    allowed_domains = ["mgsu.ru"]
    start_urls = ["https://mgsu.ru/news/announce/rss"]
    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }

    def parse(self, response, **kwargs):
        for item in response.xpath('//channel/item'):
            title = item.xpath('title//text()').extract_first()
            link = item.xpath('link//text()').extract_first()
            desc = item.xpath('description//text()').extract_first()
            if 'онференц' in title:
                yield scrapy.Request(link, meta={'desc': desc}, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_s_desc = response.meta.get('desc')
        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('conf_name', "//h2/text()")
        new_item.add_value('conf_s_desc', conf_s_desc)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', id='inner-content')
        lines = conf_block.find('div', class_='news-text').find_all(['div', 'p', 'li'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
