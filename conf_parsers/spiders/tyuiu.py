import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string, parse_vague_dates


class TyuiuSpider(scrapy.Spider):
    name = "tyuiu"
    un_name = 'Тюменский индустриальный университет'
    allowed_domains = ["www.tyuiu.ru"]
    start_urls = ["https://www.tyuiu.ru/1028-2/konferentsii-2/"]

    def parse(self, response, **kwargs):
        for row in response.css('tr'):
            try:
                _, title, date, conf_address, contacts, deadline = \
                    [i.xpath("string(.)").get() for i in row.css('td')]
            except ValueError:
                continue

            title = row.css('td')[1].xpath('concat(./text(), ./strong/text())').get()

            if 'онференц' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                dates = find_date_in_string(date)
                if not dates:
                    dates = parse_vague_dates(date)
                if dates:
                    new_item.add_value('conf_date_begin', dates[0])
                    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

                new_item.add_value('conf_name', title)
                new_item.add_value('conf_desc', title)
                new_item.add_value('conf_s_desc', title)
                new_item.add_value('conf_address', conf_address)
                new_item.add_value('contacts', contacts)
                new_item.add_value('conf_card_href', response.url)
                if reg_date_end := find_date_in_string(deadline):
                    new_item.add_value('reg_date_end', reg_date_end[0])
                if 'онлайн' in title or 'гибридн' in title.lower():
                    new_item.add_value('online', True)

                yield new_item.load_item()
