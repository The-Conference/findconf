import re
import scrapy
from scrapy.exceptions import CloseSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class SsmuSpider(scrapy.Spider):
    name = 'ssmu'
    allowed_domains = ['ssmu.ru']
    un_name = 'Сибирский Государственный Медицинский Университет'
    start_urls = ['https://ssmu.ru/ru/nauka/activity/']

    def parse(self, response, **kwargs):
        year = response.xpath("//*[contains(text(), 'планиру')]").get()
        try:
            year = re.findall(r'(\d+)', year)[0]
        except IndexError:
            raise CloseSpider('Year not found')

        for row in response.css('tr'):
            try:
                date, title, conf_address, contacts = (
                    i.xpath('string(.)').get() for i in row.css('td')
                )
                date += year
            except ValueError:
                continue

            if 'онференц' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item = get_dates(date, new_item, is_vague=True)
                new_item.add_value('title', title)
                new_item.add_value('description', title)
                new_item.add_value('conf_address', conf_address)
                new_item.add_value('contacts', contacts)
                new_item.add_value('source_href', response.url)

                if 'онлайн' in conf_address or 'гибридн' in conf_address:
                    new_item.add_value('online', True)

                yield new_item.load_item()
