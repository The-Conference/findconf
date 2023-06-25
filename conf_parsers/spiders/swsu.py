from datetime import datetime

import scrapy
from urllib.parse import unquote

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_pdf_table


class SwsuSpider(scrapy.Spider):
    name = "swsu"
    un_name = 'Юго-Западный государственный университет'
    allowed_domains = ["swsu.ru"]
    start_urls = ["https://swsu.ru/conference/"]

    def parse(self, response, **kwargs):
        current_year = str(datetime.now().year)
        link = response.xpath(f"//main[@class='work_area']//a[contains(text(), {current_year})]/@href").get()
        yield scrapy.Request(url=response.urljoin(unquote(link)), callback=self.parse_pdf)

    def parse_pdf(self, response):
        for row in parse_pdf_table(response.body):
            try:
                conf_name = row[1]
                contacts = row[3]
                dates = row[4]
            except IndexError:
                continue

            if 'конф' in conf_name.lower():
                dates = dates.replace('-\n', '')
                conf_name = conf_name.replace('-\n', '')
                contacts = contacts.replace('-\n', '')

                new_item = ConferenceLoader(item=ConferenceItem())
                new_item.add_value('conf_name', conf_name)
                new_item.add_value('conf_desc', conf_name)
                new_item.add_value('contacts', contacts)
                new_item = get_dates(dates, new_item, is_vague=True)
                yield new_item.load_item()
