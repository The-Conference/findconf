import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_plain_text


class NpiSpider(scrapy.Spider):
    name = "npi"
    un_name = 'Южно-Российский государственный политехнический университет (НПИ) имени М.И. Платова'
    allowed_domains = ["npi-tu.ru"]
    start_urls = ["https://www.npi-tu.ru/science/activities/konferentsii/"]

    def parse(self, response, **kwargs):
        for row in response.css("div.col-md-10 li"):
            conf_name = row.xpath("string(.)").get()
            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                try:
                    conf_name, date = conf_name.split('(')
                except ValueError:
                    date = conf_name
                new_item.add_value('conf_name', conf_name)
                new_item.add_value('conf_card_href', response.url)
                new_item = get_dates(date, new_item, is_vague=True)
                new_item = parse_plain_text(conf_name, new_item)
                yield new_item.load_item()
