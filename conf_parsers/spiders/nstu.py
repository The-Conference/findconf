from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class NstuSpider(CrawlSpider):
    name = "nstu"
    un_name = 'Новосибирский государственный технический университет'
    allowed_domains = ["nstu.ru"]
    start_urls = ["https://www.nstu.ru/science/scientific_events"]
    rules = (
        Rule(LinkExtractor(restrict_css="div.science-events__item-cell"),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h3::text")
        dates = response.xpath("string(//div[@class='text-bold mb-1'])").get()
        new_item = get_dates(dates, new_item)

        for line in response.xpath("//main[@class='page-content']/div/div[@class='row']"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
