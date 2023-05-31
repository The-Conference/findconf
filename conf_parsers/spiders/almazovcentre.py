from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class AlmazovcentreSpider(CrawlSpider):
    name = "almazovcentre"
    un_name = 'ФГБУ «НМИЦ им. В. А. Алмазова» Минздрава России'
    allowed_domains = ["www.almazovcentre.ru"]
    start_urls = ["http://www.almazovcentre.ru/?cat=5"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.entry-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem())

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='entry fix')

        conf_name = soup.find('article').find('div', class_='title').find('a').text
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_card_href', response.request.url)

        if side_block := conf_block.find('div', class_='personal'):
            for ref in side_block.find_all('a'):
                new_item.add_value('reg_href', ref.get('href') if 'регистрация' in ref.text.lower() else None)

        if dates := find_date_in_string(conf_name):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        lines = conf_block.find_all(['p', 'div'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
