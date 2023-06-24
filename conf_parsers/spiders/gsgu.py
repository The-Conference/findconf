import scrapy
from urllib.parse import unquote

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_pdf_table


class GsguSpider(scrapy.Spider):
    name = "gsgu"
    un_name = 'Государственный социально-гуманитарный университет'
    allowed_domains = ["gukolomna.ru"]
    start_urls = ["https://gukolomna.ru/"]

    def parse(self, response, **kwargs):
        link = response.xpath("//a[contains(text(), 'Научные мероприятия')]/@href").get()
        yield scrapy.Request(url=response.urljoin(unquote(link)), callback=self.parse_pdf)

    def parse_pdf(self, response):
        for row in parse_pdf_table(response.body):
            try:
                _, conf_name, dates, _ = row
            except ValueError:
                continue

            if 'онференц' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem())
                new_item.add_value('conf_name', conf_name)
                new_item.add_value('conf_desc', conf_name)
                new_item = get_dates(dates, new_item, is_vague=True)
                yield new_item.load_item()
