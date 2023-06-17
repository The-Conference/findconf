from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class NsuSpider(CrawlSpider):
    name = "nsu"
    un_name = 'Новосибирский национальный исследовательский государственный университет'
    allowed_domains = ["nsu.ru"]
    start_urls = ["https://www.nsu.ru/n/research/conferences/?arFilter_DATE_ACTIVE_FROM=this_year#period-filter"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.events-card > a.name', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")

        for line in response.xpath("//div[@class='detail_text']//text()"):
            new_item = default_parser_xpath(line, new_item)
        new_item.replace_xpath('conf_address', "string(//div[@class='gray-div pull-left'])")
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('conf_desc'), new_item)
        yield new_item.load_item()
