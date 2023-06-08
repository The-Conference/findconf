import re
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class UnitechMo:
    un_name = 'Технологический университет имени дважды Героя Советского Союза, летчика-космонавта А.А. Леонова'
    allowed_domains = ["unitech-mo.ru"]


class UnitechMoSpider(CrawlSpider, UnitechMo):
    name = "unitech_mo"
    start_urls = ["https://unitech-mo.ru/announcement/"]
    rules = (
        Rule(LinkExtractor(restrict_css='article', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='a.modern-page-next')),
    )
    custom_settings = {
        "DEPTH_LIMIT": 2
    }

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        new_item.add_css('conf_s_desc', "div.col-md-12::text")

        for line in response.xpath("//div[@class='container']//div[@class='col-md-12']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()


class UnitechMoSpider2(scrapy.Spider, UnitechMo):
    name = "unitech_mo2"
    start_urls = ["https://unitech-mo.ru/science/research-activities-/youth-science/calendar-of-scientific-events/"]

    def parse(self, response, **kwargs):
        year = response.xpath("//h3[contains(text(), 'Календарь')]").get()
        try:
            year = re.findall(r'(\d{4})', year)[0]
        except IndexError:
            raise CloseSpider('Year not found')

        month = ''
        for row in response.css('tr'):
            data = [cell.xpath('string(.)').get() for cell in row.css('td')]
            try:
                month, title, date = data
            except ValueError:
                title, date = data

            if 'онференц' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item = get_dates(f'{date} {month} {year}', new_item, is_vague=True)
                new_item.add_value('conf_address', re.split(r'(\d+)', date)[0])
                new_item.add_value('conf_name', title)
                new_item.add_value('conf_desc', title)
                new_item.add_value('conf_card_href', response.url)

                yield new_item.load_item()


class UnitechMoSpider3(scrapy.Spider, UnitechMo):
    name = "unitech_mo3"
    start_urls = ["https://unitech-mo.ru/science/postgraduate-study/scientific-practical-conference/"]

    def parse(self, response, **kwargs):
        container = response.css('div.container')
        for line in container.xpath('.//h4[not(@class)]'):
            title = line.xpath('string(.)').get()
            if 'конфер' in title.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item.add_value('conf_card_href', response.url)
                new_item.add_value('conf_name', title)
                date = line.xpath('./following-sibling::p')[0].get()
                desc = line.xpath('./following-sibling::p//text()')[1].get()
                new_item.add_value('conf_desc', desc)
                new_item = get_dates(date, new_item)

                yield new_item.load_item()
