import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MgsuSpider(scrapy.Spider):
    name = "mgsu"
    un_name = 'Московский государственный строительный университет'
    allowed_domains = ["mgsu.ru"]
    start_urls = ["https://mgsu.ru/news/announce/rss"]
    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }

    def parse(self, response, **kwargs):
        for item in response.xpath('//channel/item'):
            title = item.xpath('title//text()').extract_first()
            link = item.xpath('link//text()').extract_first()
            desc = item.xpath('description//text()').extract_first()
            if 'онференц' in title:
                yield scrapy.Request(link, meta={'desc': desc}, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h2/text()")
        new_item.add_value('short_description', response.meta.get('desc'))

        for line in response.xpath("//div[@class='news-text']//*[self::p or self::div or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
