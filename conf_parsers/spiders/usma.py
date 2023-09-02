from datetime import datetime
from urllib.parse import urlencode

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class UsmaSpider(CrawlSpider):
    name = "usma"
    un_name = 'Уральский государственный медицинский университет'
    allowed_domains = ["usma.ru"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.new-title'), callback="parse_items", follow=False),
    )

    def start_requests(self):
        url = "https://usma.ru/category/konferencii/?"
        querystring = {"conf_year": datetime.now().year}
        yield scrapy.Request(url=url + urlencode(querystring))

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "a.new-title-post::text")

        for line in response.xpath("//div[@class='text-news']//*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            text = response.xpath("string(//div[@class='block-new-post new-single'])").get()
            new_item = get_dates(text, new_item)

        yield new_item.load_item()
