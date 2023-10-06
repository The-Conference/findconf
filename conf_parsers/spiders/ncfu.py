from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class NcfuSpider(CrawlSpider):
    name = 'ncfu'
    un_name = 'Северо-Кавказский федеральный университет'
    allowed_domains = ['ncfu.ru']
    start_urls = [
        'https://www.ncfu.ru/science/scientific-events/',
        # "https://www.ncfu.ru/science/scientific-events/Proedie-meropriyatiya/"
    ]
    rules = (
        Rule(
            LinkExtractor(restrict_css='div.static-content li', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', 'h1.h4::text')

        for line in response.xpath(
            "//div[@class='static-content']//*[self::p or self::ul or self::ol]"
        ):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.meta.get('link_text'), new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('description'), new_item)

        yield new_item.load_item()
