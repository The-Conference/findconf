import scrapy
import pdfplumber
from io import BytesIO
from urllib.parse import unquote
import logging

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates

# pdfplumber logs are extremely verbose
logging.getLogger("pdfminer").setLevel(logging.WARNING)


class GsguSpider(scrapy.Spider):
    name = "gsgu"
    un_name = 'Государственный социально-гуманитарный университет'
    allowed_domains = ["gukolomna.ru"]
    start_urls = ["https://gukolomna.ru/"]

    def parse(self, response, **kwargs):
        link = response.xpath("//a[contains(text(), 'Научные мероприятия')]/@href").get()
        yield scrapy.Request(url=response.urljoin(unquote(link)), callback=self.parse_pdf)

    def parse_pdf(self, response):
        f = BytesIO(response.body)
        pdf = pdfplumber.open(f)
        for page in pdf.pages:
            for row in page.extract_table():
                try:
                    n, conf_name, dates, _ = row
                    float(n)
                except ValueError:
                    continue
                if 'онференц' in conf_name.lower():
                    new_item = ConferenceLoader(item=ConferenceItem())
                    new_item.add_value('conf_name', conf_name)
                    new_item.add_value('conf_desc', conf_name)
                    new_item = get_dates(dates, new_item)
                    yield new_item.load_item()
