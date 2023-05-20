import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class BashgmuSpider(scrapy.Spider):
    name = "bashgmu"
    un_name = 'Башкирский государственный медицинский университет'
    allowed_domains = ["bashgmu.ru"]
    start_urls = ["https://bashgmu.ru/science_and_innovation/konferentsii/"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='p.grants-item', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
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
            lowercase = line.text.lower()
            new_item.add_value('conf_desc', line.get_text(separator=" "))

            if 'состоится' in lowercase or 'открытие' in lowercase or 'проведен' in lowercase:
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('conf_date_begin', dates[0].date())
                    new_item.add_value('conf_date_end', dates[1].date() if len(dates) > 1 else dates[0].date())

            if ('заявк' in lowercase or 'принимаютс' in lowercase or 'регистрац' in lowercase or
                'регистрир' in lowercase):
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('reg_date_begin', dates[0].date())
                    new_item.add_value('reg_date_end', dates[1].date() if 1 < len(dates) else None)

            if 'регистрац' in lowercase or 'зарегистр' in lowercase or 'участия' in lowercase or 'заявк' in lowercase:
                new_item.add_value(
                    'reg_href', line.find('a').get('href')
                    if line.find('a') and (
                            'http:' in line.find('a').get('href') or 'https:' in line.find('a').get('href')) and (
                               '.pdf' not in line.find('a').get('href') or
                               '.doc' not in line.find('a').get('href') or
                               '.xls' not in line.find('a').get('href')) else None)

            if 'организатор' in lowercase:
                new_item.add_value('org_name', line.get_text(separator=" "))

            if 'онлайн' in lowercase or 'трансляц' in lowercase:
                new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else None)
                new_item.add_value('online', True)

            if 'место' in lowercase or 'адрес' in lowercase:
                new_item.add_value('conf_address', line.text)
                new_item.add_value('offline', True)

            if ('тел.' in lowercase or 'контакт' in lowercase or 'mail' in lowercase
                    or 'почта' in lowercase or 'почты' in lowercase):
                new_item.add_value('contacts', line.text)

            if line.find('a') and 'mailto' in line.find('a').get('href'):
                new_item.add_value('contacts', line.text)

            new_item.add_value('rinc', True if 'ринц' in lowercase else False)

        yield new_item.load_item()
