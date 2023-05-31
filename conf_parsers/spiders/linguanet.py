import datetime
import scrapy
from bs4 import BeautifulSoup
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class LinguanetSpider(scrapy.Spider):
    name = "linguanet"
    un_name = 'Московский государственный лингвистический университет'
    allowed_domains = ["www.linguanet.ru"]
    start_urls = [
        "https://www.linguanet.ru/science/konferentsii-i-seminary/",
        "https://www.linguanet.ru/science/konferentsii-i-seminary/konferentsii-v-drugikh-vuzakh/"
    ]

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        main_container = soup.find('div', class_='page col-xs-12 col-sm-9')
        container1 = main_container.find_all(['p', 'div'])
        for line in container1:
            conf_name = line.get_text(separator=" ")
            if 'конфер' in conf_name:
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
                new_item.add_value('conf_name', conf_name)
                if conf_name == 'Ссылка на официальный сайт конференции   Информационное письмо':
                    continue
                new_item.add_value('conf_s_desc', conf_name)
                new_item.add_value('conf_desc', conf_name)
                dates = find_date_in_string(conf_name)
                if dates:
                    new_item.add_value('conf_date_begin', dates[0])
                    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
                    if dates[0].year < datetime.datetime.now().year:
                        break

                for i in line.find_all('a'):
                    if 'регистрац' in i.text.lower():
                        new_item.add_value('reg_href', i.get('href'))
                    if 'информационное' in i.text.lower() or 'подробнее' in i.text.lower():
                        new_item.add_value('conf_card_href', 'https://www.linguanet.ru' + i.get('href'))
                    if 'ссылка на официальный' in i.text.lower():
                        new_item.add_value('conf_card_href', i.get('href'))
                yield new_item.load_item()

        container2 = main_container.find_all('div', class_='news-index clearfix')
        for line in container2:
            conf_card_href = 'https://www.linguanet.ru' + line.find('a').get('href')
            conf_s_desc = line.get_text(separator=" ")
            if 'конфер' in line.get_text(separator=" ").lower():
                yield scrapy.Request(conf_card_href, meta={'desc': conf_s_desc}, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('conf_name', "//h1/text()")
        new_item.add_value('conf_s_desc', response.meta.get('desc'))

        soup = BeautifulSoup(response.text, 'lxml')
        main_container = soup.find('div', class_='page col-xs-12 col-sm-9')
        main_container = main_container.find_all(['div', 'p'])
        for line in main_container:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
