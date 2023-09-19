import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class HseSpider(scrapy.Spider):
    name = "hse"
    un_name = 'Национальный исследовательский университет «Высшая школа экономики»'
    allowed_domains = ["hse.ru"]
    start_urls = ["https://www.hse.ru/news/announcements/scientific_actions/?cbtype2=on"]

    def parse(self, response, **kwargs):
        for item in response.css("div.b-events__body"):
            title = item.xpath("string(./div[@class='b-events__body_title large'])").get()
            link = item.xpath(".//a/@href").get()
            if 'онференц' in title.lower():
                yield scrapy.Request(link, callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h1/text()")
        dates = response.xpath("string(//div[contains(@class, 'g-day__title')])").get()
        new_item = get_dates(dates, new_item)

        conf_block = response.xpath("//div[@class='post__text' or "
                                    "@class='builder-section builder-section--with_indent0']")
        for line in conf_block.xpath(".//*[self::p or self::div[@class='incut']]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            dates = response.xpath("//div[@class='title u']/text()").get() or new_item.get_output_value('description')
            new_item = get_dates(dates, new_item)
        yield new_item.load_item()
