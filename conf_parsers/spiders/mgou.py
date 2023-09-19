import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class MgouSpider(scrapy.Spider):
    name = "mgou"
    un_name = 'Государственный университет просвещения'
    allowed_domains = ["mgou.ru"]
    start_urls = ["https://mgou.ru/ru/rubric/science/organizatsiya-nauchno-issledovatelskoj-deyatelnosti-mgou-2"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//div[@class='customTable']//tr"):
            try:
                _, conf_name, date, _ = [i.xpath("string(.)").get() for i in row.css('td')]
            except ValueError:
                continue

            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item = get_dates(date, new_item, is_vague=True)
                new_item.add_value('title', conf_name)
                new_item.add_value('description', conf_name)
                if 'онлайн' in conf_name or 'интернет' in conf_name:
                    new_item.add_value('online', True)

                yield new_item.load_item()
