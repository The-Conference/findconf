import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_conf


class SamgtuSpider(scrapy.Spider):
    name = "samgtu"
    un_name = 'Самарский государственный технический университет'
    allowed_domains = ["samgtu.ru"]
    start_urls = ["https://samgtu.ru/conferences"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//div[@class='text-block']//tr"):
            try:
                title, date = [i.xpath("string(.)").get() for i in row.css('td')]
            except ValueError:
                continue
            if 'конфер' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item.add_value('title', title)
                new_item.add_value('source_href', response.url)
                new_item = get_dates(date, new_item, is_vague=True)
                new_item = parse_conf(title, new_item)
                yield new_item.load_item()
