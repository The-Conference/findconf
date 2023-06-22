from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class RushSpider(CrawlSpider):
    name = "rush"
    un_name = 'Российский государственный гуманитарный университет'
    allowed_domains = ["rsuh.ru"]
    start_urls = ["https://www.rsuh.ru/anons/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.news_box > a', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h2.zagol::text")
        new_item.add_xpath('conf_s_desc', "string(//div[@class='col-sm-8']/p)")

        for line in response.xpath("//div[@class='col-xl-12']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('conf_s_desc'), new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            dates = response.xpath("string(//div[@class='col-sm-8']/strong)").get()
            new_item = get_dates(dates, new_item)
        yield new_item.load_item()
