from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from urllib.parse import unquote
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class A1spbgmuSpider(CrawlSpider):
    name = "1spbgmu"
    un_name = 'Первый Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова'
    allowed_domains = ["www.1spbgmu.ru"]
    start_urls = ["https://www.1spbgmu.ru/nauka/konferentsii"]
    rules = (
        Rule(LinkExtractor(restrict_css='td.list-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem())
        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='item-page')

        conf_name = conf_block.find('div', class_='page-header').get_text(separator=" ")
        new_item.add_value('conf_name', conf_name)
        prev_text = ''
        new_item.add_value('conf_card_href', unquote(response.url))
        if dates := find_date_in_string(conf_name):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

        for line in conf_block.find('div', itemprop='articleBody').find_all('p'):
            lowercase = line.text.lower()
            new_item.add_value('conf_desc', line.get_text(separator=" "))
            if 'коллеги' in prev_text.lower():
                new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            if 'регистрац' in lowercase:
                new_item.add_value('reg_href', line.find('a').get('href') if line.find('a') else None)
            if 'организатор' in lowercase:
                new_item.add_value('org_name', line.get_text(separator=" "))
            if 'онлайн' in lowercase or 'трансляц' in lowercase:
                new_item.add_value('online', True)
                new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else None)
            if 'место' in lowercase or 'адрес' in lowercase:
                new_item.add_value('offline', True)
                new_item.add_value('conf_address', line.get_text(separator=" "))
            if ('телеф' in lowercase or 'контакт' in lowercase or 'mail' in lowercase
                    or 'почта' in lowercase or 'почты' in lowercase):
                new_item.add_value('contacts', line.get_text(separator=" "))

            if line.find('a'):
                for a in line.find_all('a'):
                    if 'mailto' in a.get('href'):
                        new_item.add_value('contacts', a.text)

            if 'заявки' in lowercase or 'принимаютс' in lowercase or 'регистрац' in lowercase:
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('reg_date_begin', dates[0])
                    new_item.add_value('reg_date_end', dates[1] if 1 < len(dates) else None)

            new_item.add_value('rinc', True if 'ринц' in lowercase else False)
            new_item.add_value('scopus', True if 'scopus' in lowercase else False)
            new_item.add_value('vak', True if 'ВАК' in line.text else False)
            new_item.add_value('wos', True if 'wos' in lowercase else False)
            prev_text = lowercase

        yield new_item.load_item()
