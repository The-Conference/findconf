import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_conf


class NpiSpider(scrapy.Spider):
    name = 'npi'
    un_name = 'Южно-Российский государственный политехнический университет (НПИ) имени М.И. Платова'
    allowed_domains = ['npi-tu.ru']
    start_urls = ['https://www.npi-tu.ru/science/activities/konferentsii/']

    def parse(self, response, **kwargs):
        for row in response.css('div.col-md-10 li'):
            conf_name = row.xpath('string(.)').get()
            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                try:
                    conf_name, date = conf_name.split('(')
                except ValueError:
                    date = conf_name
                new_item.add_value('title', conf_name)
                new_item.add_value('source_href', response.url)
                new_item = get_dates(date, new_item, is_vague=True)
                new_item = parse_conf(conf_name, new_item)
                yield new_item.load_item()
