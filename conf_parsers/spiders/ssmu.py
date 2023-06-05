import re
import scrapy
from scrapy.exceptions import CloseSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class SsmuSpider(scrapy.Spider):
    name = "ssmu"
    allowed_domains = ["ssmu.ru"]
    un_name = 'Сибирский Государственный Медицинский Университет'
    start_urls = ["https://ssmu.ru/ru/nauka/activity/"]

    def parse(self, response, **kwargs):
        year = response.xpath("//*[contains(text(), 'планиру')]").get()
        try:
            year = re.findall(r'(\d+)', year)[0]
        except IndexError:
            raise CloseSpider('Year not found')
        for row in response.css('tr'):
            cells = row.css('td')
            date = cells[0].xpath("string(.)").get() + year
            title = cells[1].xpath("string(.)").get()
            conf_address = cells[2].xpath("string(.)").get()
            contacts = cells[3].xpath("string(.)").get()

            if 'онференц' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item = get_dates(date, new_item, is_vague=True)
                new_item.add_value('conf_name', title)
                new_item.add_value('conf_desc', title)
                new_item.add_value('conf_s_desc', title)
                new_item.add_value('conf_address', conf_address)
                new_item.add_value('contacts', contacts)
                new_item.add_value('conf_card_href', response.url)
                new_item.add_value('org_name', cells[3].css('p:nth-of-type(2)::text').get())

                if 'онлайн' in conf_address or 'гибридн' in conf_address:
                    new_item.add_value('online', True)

                yield new_item.load_item()
