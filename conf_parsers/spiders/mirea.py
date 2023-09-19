import re
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates
from ..utils import normalize_string


class MireaSpider(scrapy.Spider):
    name = "mirea"
    un_name = 'МИРЭА — Российский технологический университет'
    allowed_domains = ["mirea.ru"]
    start_urls = ["https://www.mirea.ru/nauka-i-innovatsii/seminars-and-conferences/"]

    def parse(self, response, **kwargs):
        data = response.xpath("//div[@class='uk-width-1-1']//text()")
        rows = [normalize_string(row.get()) for row in data]
        clean = [i for i in rows if i != '']
        collected_confs = []
        conf = dict()
        for i, row in enumerate(clean):
            text = row.lower()
            if not re.findall(r'^(?![\s\S])', text):
                if 'дата' in text:
                    collected_confs.append(conf)
                    conf = dict()
                    conf['title'] = clean[i - 1]
                    conf['date'] = clean[i + 1]
                elif 'место' in text:
                    conf['addr'] = clean[i + 1]
                elif 'организатор' in text:
                    conf['org'] = clean[i + 1]
                elif 'формат' in text:
                    conf['form'] = clean[i + 1]
                else:
                    continue

        for conf in collected_confs:
            if conf and ('конф' in conf.get('form').lower() or
                         'конф' in conf.get('title').lower()):
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)

                new_item.add_value('source_href', response.url)
                new_item.add_value('title', conf.get('title'))
                new_item = get_dates(conf.get('date'), new_item, is_vague=True)
                new_item = default_parser_xpath(conf.get('title'), new_item)
                new_item.add_value('org_name', conf.get('org'))
                new_item.add_value('conf_address', conf.get('addr'))

                yield new_item.load_item()
