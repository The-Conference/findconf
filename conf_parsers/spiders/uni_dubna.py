import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates
from ..utils import find_date_in_string


class UniDubnaSpider(scrapy.Spider):
    name = "uni_dubna"
    un_name = 'Государственный университет "Дубна"'
    allowed_domains = ["uni-dubna.ru"]
    start_urls = ["https://conf.uni-dubna.ru/Home/Conferences"]

    def parse(self, response, **kwargs):
        for conf in response.css('div.card-body'):
            link = conf.css('a::attr(href)').get()
            date = find_date_in_string(conf.css('h5').get())
            if date[0] >= self.settings.get('FILTER_DATE'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1.title_one::text")
        new_item.add_xpath('conf_s_desc', "string(//h5[@class='description info1'])")
        dates_select = response.xpath("string(//h4[@class='hero-text-small'])").get()
        new_item = get_dates(dates_select, new_item)

        for line in response.xpath("//div[@class='container']//*[self::p or self::h3 or self::h5]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
