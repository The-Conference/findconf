import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class MgouSpider(scrapy.Spider):
    name = "mgou"
    un_name = 'Московский государственный областной педагогический университет'
    allowed_domains = ["mgou.ru"]
    start_urls = ["https://mgou.ru/ru/rubric/science/organizatsiya-nauchno-issledovatelskoj-deyatelnosti-mgou-2"]

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        main_container = soup.find('div', class_='_1n2mji8by _1n2mji8bz _1n2mji8c2')
        tables = main_container.find_all('div', class_='customTable')

        for table in tables:
            for line in table.find_all('tr'):
                if line.find('td').text == '№':
                    continue
                if line.find_all('td')[0].text == line.find_all('td')[-1].text:
                    continue
                if 'конфер' in line.find_all('td')[1].text.lower():
                    new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
                    dates = line.find_all('td')[2].text
                    new_item = get_dates(dates, new_item, is_vague=True)
                    conf_name = line.find_all('td')[1].text
                    new_item.add_value('conf_name', conf_name)
                    new_item.add_value('conf_s_desc', conf_name)
                    new_item.add_value('conf_desc', conf_name)

                    new_item.add_value('org_name', line.find_all('td')[3].text)
                    if 'онлайн' in conf_name or 'интернет' in conf_name:
                        new_item.add_value('online', True)

                    yield new_item.load_item()
