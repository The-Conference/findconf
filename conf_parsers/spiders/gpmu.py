from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class GpmuSpider(CrawlSpider):
    name = "gpmu"
    un_name = 'Санкт-Петербургский государственный педиатрический медицинский университет'
    allowed_domains = ["gpmu.org"]
    start_urls = ["https://gpmu.org/science/conference/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.catinfo_item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1)")
        new_item.add_xpath('title', "string(//div[@class='title_cont'])")
        table_date = response.xpath("string(//div[@id='content']//td)").get()
        new_item = get_dates(table_date, new_item)

        lines = response.xpath("//div[@id='content']/*[self::p or self::ul or self::div]")
        for line in lines:
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
