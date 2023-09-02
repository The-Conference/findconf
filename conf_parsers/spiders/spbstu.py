from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class SpbstuSpider(CrawlSpider):
    name = "spbstu"
    un_name = 'Санкт-Петербургский политехнический университет Петра Великого'
    allowed_domains = ["www.spbstu.ru"]
    start_urls = ["https://www.spbstu.ru/media/announcements/conference/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event-desc', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")

        for line in response.xpath("//div[@id='content_page']/*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            dates = response.xpath("string(//div[@class='event-inf'])").get()
            new_item = get_dates(dates, new_item)

        yield new_item.load_item()
