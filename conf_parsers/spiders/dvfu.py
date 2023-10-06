from urllib.parse import urlencode
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class DvfuSpider(CrawlSpider):
    name = 'dvfu'
    un_name = 'Дальневосточный федеральный университет'
    allowed_domains = ['dvfu.ru']
    start_urls = ['https://www.dvfu.ru/science/scientific-events/?tags=конференция']
    rules = (
        Rule(
            LinkExtractor(restrict_css='div.news-item', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
    )

    def start_requests(self):
        url = 'https://www.dvfu.ru/science/scientific-events/?'
        current_year = str(datetime.now().year)
        current_month = datetime.now().month
        for i in range(current_month, 13):
            querystring = {'MONTH': str(i), 'YEAR': current_year}
            yield scrapy.Request(url=url + urlencode(querystring))

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', 'div.news-item-title::text')

        for line in response.xpath("//div[@class='news-item-full']/text()"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
