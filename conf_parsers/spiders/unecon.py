from urllib.parse import urlencode
import scrapy
from scrapy.exceptions import CloseSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath
from ..utils import find_date_in_string


class UneconSpider(scrapy.Spider):
    name = "unecon"
    un_name = "Санкт-Петербургский государственный экономический университет"
    allowed_domains = ["unecon.ru"]
    start_urls = ["https://unecon.ru/wp-json/unecon/v1/announcements?"]
    params = {
        'page': 1,
        'category': 212,
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0] + urlencode(self.params), callback=self.parse)

    def parse(self, response, **kwargs):
        jsonresponse = response.json().get('list')
        if not jsonresponse:
            raise CloseSpider('All done')

        for item in jsonresponse:
            title = item.get('title')
            link = item.get('link')
            date_start = item.get('date_start')
            date_end = item.get('date_end')
            yield scrapy.Request(link, callback=self.parse_items,
                                 meta={'title': title,
                                       'date_start': date_start,
                                       'date_end': date_end})

        self.params['page'] = int(self.params['page']) + 1
        yield scrapy.Request(self.start_urls[0] + urlencode(self.params), callback=self.parse)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_value('conf_name', response.meta.get('title'))
        conf_s_desc = response.xpath("string(//div[@class='post_content']/p)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        conf_date_begin = find_date_in_string(response.meta.get('date_start'))
        conf_date_end = find_date_in_string(response.meta.get('date_end'))
        new_item.add_value('conf_date_begin', conf_date_begin[0])
        new_item.add_value('conf_date_end', conf_date_end[0])

        for line in response.xpath("//div[@class='post_content']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
