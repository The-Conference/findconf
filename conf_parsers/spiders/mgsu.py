import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class MgsuSpider(scrapy.Spider):
    name = "mgsu"
    un_name = 'Московский городской педагогический университет'
    allowed_domains = ["mgsu.ru"]
    start_urls = ["https://mgsu.ru/news/announce/rss"]
    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response, **kwargs):
        for item in response.xpath('//channel/item'):
            title = item.xpath('title//text()').extract_first()
            link = item.xpath('link//text()').extract_first()
            desc = item.xpath('description//text()').extract_first()
            if 'онференц' in title:
                yield scrapy.Request(link, meta={'desc': desc}, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_s_desc = response.meta.get('desc')
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h2/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_s_desc)
        new_item.add_value('local', False if 'международн' in conf_name else True)

        conf_block = soup.find('div', id='inner-content')
        lines = conf_block.find('div', class_='news-text').find_all(['div', 'p', 'li'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            if dates := find_date_in_string(conf_s_desc):
                new_item.add_value('conf_date_begin', dates[0])
                new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
        yield new_item.load_item()
