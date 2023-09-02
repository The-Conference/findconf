import re
from datetime import datetime
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_plain_text


class GuuSpider(scrapy.Spider):
    name = "guu"
    un_name = 'Государственный университет управления'
    allowed_domains = ["guu.ru"]
    start_urls = ["https://guu.ru/science/scince_events/"]

    def parse(self, response, **kwargs):
        current_year = datetime.now().year
        for table in response.css("table"):
            year = table.xpath("string(.//tr/td[position()=3])").get()
            year = int(re.findall(r'\d+', year)[0])
            if year < current_year:
                break
            for row in table.css("tr"):
                try:
                    _, conf_name, dates, contacts, _ = [i.xpath("string(.)").get() for i in row.css('td')]
                except ValueError:
                    continue
                if 'конфер' in conf_name.lower():
                    new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                    new_item.add_value('title', conf_name)
                    new_item.add_value('source_href', response.url)
                    new_item.add_value('contacts', contacts)
                    new_item = get_dates(dates, new_item, is_vague=True)
                    new_item = parse_plain_text(conf_name, new_item)
                    yield new_item.load_item()
