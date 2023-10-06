from datetime import datetime
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class VsuSpider(CrawlSpider):
    name = 'vsu'
    un_name = 'Воронежский государственный университет'
    allowed_domains = ['vsu.ru']
    rules = (
        Rule(
            LinkExtractor(restrict_css='div.content td > a', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
    )

    def start_requests(self):
        url = 'http://www.science.vsu.ru/selconf'
        year = str(datetime.now().year)
        payload = {
            'start_month': '1',
            'start_year': year,
            'end_month': '12',
            'end_year': year,
            'period_sub': 'Выбрать',
        }
        yield scrapy.FormRequest(url, formdata=payload)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', 'div.confername::text')

        for line in response.xpath("//div[@class='stickybody']"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
