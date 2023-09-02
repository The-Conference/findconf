import re
from datetime import datetime

import scrapy
from scrapy.exceptions import CloseSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class RusoilSpider(scrapy.Spider):
    name = "rusoil"
    un_name = 'Уфимский государственный нефтяной технический университет'
    allowed_domains = ["rusoil.net"]
    start_urls = ["https://rusoil.net/ru/page/konferencii-i-simpoziumy"]

    def parse(self, response, **kwargs):
        year = response.xpath("string(//h3)").get()
        year = re.findall(r'\d+', year)[0]
        if int(year) < datetime.now().year:
            raise CloseSpider('No new items.')

        for row in response.xpath("//table[@class='article__table']//tr"):
            try:
                _, title, dates, contacts = [i.xpath("string(.)").get() for i in row.css('td')]
                dates += year
            except ValueError:
                continue

            if 'онференц' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item.add_value('source_href', response.url)
                new_item.add_value('title', title)
                new_item = get_dates(dates, new_item, is_vague=True)
                new_item = default_parser_xpath(title, new_item)
                new_item.add_value('contacts', contacts)

                yield new_item.load_item()
