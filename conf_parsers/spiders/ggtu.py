import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_conf


class GgtuSpider(scrapy.Spider):
    name = 'ggtu'
    un_name = 'Государственный гуманитарно-технологический университет'
    allowed_domains = ['www.ggtu.ru']
    start_urls = [
        'https://www.ggtu.ru/index.php?option=com_content&view=article&id=9230&Itemid=810'
    ]

    def parse(self, response, **kwargs):
        for row in response.xpath("//div[@class='art-article']//tr"):
            try:
                conf_name, date = (i.xpath('string(.)').get() for i in row.css('td'))
            except ValueError:
                continue
            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item.add_value('title', conf_name)
                new_item.add_value('source_href', response.url)
                new_item = get_dates(date, new_item)
                new_item = parse_conf(conf_name, new_item)
                yield new_item.load_item()
