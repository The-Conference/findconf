import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class AsuSpider(scrapy.Spider):
    name = "asu"
    un_name = 'Алтайский государственный университет'
    allowed_domains = ["asu.ru"]
    start_urls = ["https://www.asu.ru/science/sci_events/"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//div[@class='tabl_events']//tr"):
            r = [i.xpath("string(.)").get() for i in row.xpath(".//td")]
            try:
                conf_type = r[1]
                title, dates, contacts = r[3:6]
                orgs, desc1, desc2 = r[8:11]
            except (IndexError, ValueError):
                continue

            if 'онференц' in conf_type.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item.add_value('source_href', response.url)
                new_item.add_value('title', title)
                new_item = get_dates(dates, new_item, is_vague=True)
                new_item = default_parser_xpath(desc1, new_item)
                new_item = default_parser_xpath(desc2, new_item)
                new_item.add_value('contacts', contacts)
                new_item.add_value('org_name', orgs)

                yield new_item.load_item()
