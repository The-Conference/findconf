import datetime
import re
import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string
from dateparser import parse


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
                    dates = find_date_in_string(line.find_all('td')[2].text)
                    if not dates:
                        dates = self.parse_vague_dates(line.find_all('td')[2].text)
                    conf_date_begin = dates[0] if len(dates) > 0 else ''
                    conf_date_end = dates[1] if len(dates) > 1 else conf_date_begin
                    new_item.add_value('conf_date_begin', conf_date_begin)
                    new_item.add_value('conf_date_end', conf_date_end)

                    conf_name = line.find_all('td')[1].text
                    new_item.add_value('conf_name', conf_name)

                    new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
                    new_item.add_value('conf_id',
                                       f"{self.name}_{line.find_all('td')[0].text}_"
                                       f"{conf_date_begin}_{conf_date_end}")
                    new_item.add_value('conf_s_desc', conf_name)
                    new_item.add_value('conf_desc', conf_name)

                    new_item.add_value('org_name', line.find_all('td')[3].text)
                    if 'онлайн' in conf_name or 'интернет' in conf_name:
                        new_item.add_value('online', True)

                    yield new_item.load_item()

    def parse_vague_dates(self, string: str) -> list[datetime.date]:
        # TODO handle this in date finder?
        string = re.sub(r'[\u002D\u058A\u05BE\u1400\u1806'
                        r'\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40'
                        r'\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D]', ' ', string)
        string = ' '.join(string.split()).split()
        month1 = month2 = year = None
        if len(string) == 2:
            month1, year = string
        elif len(string) == 3:
            month1, month2, year = string
        res = [f'01 {month1} {year}', f'{month2 or month1} {year}']
        return [parse(r, settings={'DEFAULT_LANGUAGES': ['ru'],
                                   'DATE_ORDER': 'DMY',
                                   'PREFER_DAY_OF_MONTH': 'last'}).date() for r in res]