from datetime import datetime

import scrapy
from urllib.parse import unquote

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_pdf_table


class KantianaSpider(scrapy.Spider):
    name = 'kantiana'
    un_name = 'Балтийский федеральный университет имени Иммануила Канта'
    allowed_domains = ['kantiana.ru']
    start_urls = ['https://kantiana.ru/science/nauchnye-meropriyatiya-i-konferentsii/']

    def parse(self, response, **kwargs):
        current_year = str(datetime.now().year)
        link = response.xpath(
            f"//a[@class='link--doc'][contains(text(), {current_year})]/@href"
        ).get()
        yield scrapy.Request(url=response.urljoin(unquote(link)), callback=self.parse_pdf)

    def parse_pdf(self, response):
        for row in parse_pdf_table(response.body):
            try:
                date_start, date_end, conf_name, conf_desc = row[0:4]
                conf_address = row[6]
                contacts = row[10]
            except IndexError:
                continue

            if 'конф' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)
                new_item.add_value('title', conf_name)
                new_item.add_value('source_href', self.start_urls[0])
                new_item.add_value('description', conf_desc)
                new_item.add_value('contacts', contacts)
                new_item.add_value('conf_address', conf_address)
                dates = f'{date_start} {date_end}'
                dates = dates.replace('\n', '')
                new_item = get_dates(dates, new_item, is_vague=True)

                yield new_item.load_item()
