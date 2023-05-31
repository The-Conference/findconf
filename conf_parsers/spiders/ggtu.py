import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class GgtuSpider(scrapy.Spider):
    name = "ggtu"
    un_name = 'Государственный гуманитарно-технологический университет'
    allowed_domains = ["www.ggtu.ru"]
    start_urls = ["https://www.ggtu.ru/index.php?option=com_content&view=article&id=9230&Itemid=810"]

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        main_container = soup.find('div', class_='art-article').find('tbody')

        for line in main_container.find_all('tr'):
            conf_name = ''
            conf_date_begin = None
            conf_date_end = None
            new_item = ConferenceLoader(item=ConferenceItem())
            if 'мероприятие' in line.find('td').text.lower():
                continue
            if line.find_all('td')[0].text == line.find_all('td')[-1].text:
                continue
            if 'конфер' in line.find_all('td')[0].text.lower():
                conf_name = line.find_all('td')[0].text

            if dates := find_date_in_string(line.find_all('td')[-1].text):
                conf_date_begin = dates[0]
                conf_date_end = dates[1] if len(dates) > 1 else dates[0]

            new_item.add_value('conf_card_href', self.allowed_domains[0] + line.find('a', href=True)['href'])
            new_item.add_value('conf_name', conf_name)
            new_item.add_value('conf_s_desc', conf_name)
            new_item.add_value('conf_desc', conf_name)
            new_item.add_value('conf_date_begin', conf_date_begin)
            new_item.add_value('conf_date_end', conf_date_end)
            yield new_item.load_item()
