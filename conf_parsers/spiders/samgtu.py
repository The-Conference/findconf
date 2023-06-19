import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_plain_text


class SamgtuSpider(scrapy.Spider):
    name = "samgtu"
    un_name = 'Самарский государственный технический университет'
    allowed_domains = ["samgtu.ru"]
    start_urls = ["https://samgtu.ru/conferences"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//div[@class='text-block']//tr"):
            try:
                conf_name, date = [i.xpath("string(.)").get() for i in row.css('td')]
            except ValueError:
                continue
            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item.add_value('conf_name', conf_name)
                new_item.add_value('conf_card_href', response.url)
                new_item = get_dates(date, new_item, is_vague=True)
                new_item = parse_plain_text(conf_name, new_item)
                yield new_item.load_item()
