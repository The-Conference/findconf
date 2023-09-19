from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class RudnSpider(CrawlSpider):
    name = "rudn"
    un_name = 'Российский университет дружбы народов имени Патриса Лумумбы'
    allowed_domains = ["rudn.ru"]
    start_urls = ["https://www.rudn.ru/science/conferences?format=97015975-d294-42d8-857a-0aad48ef7390"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.events__link'), callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.page__next.page__item')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        new_item.add_css('conf_address', "div.conf-det__place-address::text")
        new_item.add_css('contacts', "div.conf-det__card-person_info_email::text")
        new_item.add_css('contacts', "div.conf-det__card-person_info_phone::text")

        addr = new_item.get_output_value('conf_address').lower()
        online = True if 'online' in addr else False
        new_item.add_value('online', online)
        if addr == 'online' or addr == 'участие online':
            new_item.add_value('offline', False)

        for line in response.css("div.WYSIWYG ul,p"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.css("div.conf-det__date-date::text").get(), new_item)

        yield new_item.load_item()
