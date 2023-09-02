import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates
from ..utils import find_date_in_string


class MaiSpider(scrapy.Spider):
    name = "mai"
    un_name = 'Российский национальный исследовательский медицинский университет имени Н.И. Пирогова'
    allowed_domains = ["mai.ru"]
    start_urls = ["https://mai.ru/science/events/conf/"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//table//tr"):
            cells = row.css('td')
            try:
                date = cells[0].xpath("string(.)").get()
                link = cells[1].css("a::attr(href)").get()
                conf_name = cells[1].xpath("string(.)").get()
            except IndexError:
                continue
            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item.add_value('title', conf_name)
                new_item.add_value('source_href', response.url)
                new_item.add_value('conf_href', link)
                new_item = get_dates(date, new_item, is_vague=True)

                yield new_item.load_item()


class MaiSpider2(CrawlSpider):
    name = "mai2"
    un_name = 'Российский национальный исследовательский медицинский университет имени Н.И. Пирогова'
    allowed_domains = ["mai.ru"]
    start_urls = ["https://mai.ru/science/events/date/#"]
    rules = (
        Rule(LinkExtractor(restrict_css='ul.step a.mb-2.fw-semi-bold', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")

        for line in response.xpath("//article//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)

        citing = {'ринц': 'rinc', 'вак': 'vak'}
        for prop in response.xpath("//dl[@class='row']/dt"):
            name = prop.xpath("./text()").get()
            value = prop.xpath("./following-sibling::dd")
            text = value.xpath("string(.)").get()
            if 'Город' == name:
                new_item.replace_value('conf_address', text)
            elif 'Дата' == name:
                new_item.add_value('conf_date_begin', find_date_in_string(text)[0] or None)
            elif 'Дата окончания' == name:
                new_item.add_value('conf_date_end', find_date_in_string(text)[0] or None)
            elif 'Дата окончания приёма документов' == name:
                new_item.add_value('reg_date_end', find_date_in_string(text)[0] or None)
            elif 'Сайт' == name:
                new_item.add_value("conf_href", value.css("a::attr(href)").get())
            elif 'Публикация' in name:
                val = name.split()[-1].lower()
                val = citing.get(val) or val
                new_item.add_value(val, True)

        yield new_item.load_item()
