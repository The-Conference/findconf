from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath
from ..utils import find_date_in_string


class SguSpider(CrawlSpider):
    name = 'sgu'
    un_name = 'Саратовский национальный исследовательский государственный университет имени Н.Г. Чернышевского'
    allowed_domains = ['www.sgu.ru']
    start_urls = ['https://www.sgu.ru/conference']
    rules = (
        Rule(
            LinkExtractor(restrict_css='td.views-field-name-field-et', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
        Rule(LinkExtractor(restrict_css='li.pager-next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        conf_name = response.css('div.field-name-name-field').xpath('string(.)').get()
        new_item.add_value('title', conf_name)
        dates = response.css('div.field_conf_when').xpath('string(.)').get()
        new_item = get_dates(dates, new_item)

        for line in response.css('div.field-type-text-with-summary').css('p,ul,ol,div'):
            new_item = default_parser_xpath(line, new_item)

        side_block = response.css('div.logo_dates')
        reg_date_end = side_block.xpath("string(.//span[@property='dc:date'])").get()
        if dates := find_date_in_string(reg_date_end):
            new_item.add_value('reg_date_end', dates[0])
        contacts = (
            side_block.css('div.field-name-field-servicechanne-contacts').xpath('string(.)').get()
        )
        new_item.add_value('contacts', contacts)

        yield new_item.load_item()
