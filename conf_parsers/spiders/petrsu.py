import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class PetrsuSpider(scrapy.Spider):
    name = "petrsu"
    un_name = 'Петрозаводский государственный университет'
    allowed_domains = ["conf.petrsu.ru"]
    start_urls = ["https://conf.petrsu.ru/index.php"]

    def parse(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_css('conf_name', 'div#conf_name::text')
        new_item.add_value('conf_card_href', response.url)
        conf_s_desc = response.css('p::text').get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        dates = response.xpath("string(//div[@id='conf_name'])").get()
        new_item = get_dates(dates, new_item)

        for line in response.xpath("//div[@id='conf_desc']//*[self::p or self::div or self::table]"):
            new_item = default_parser_xpath(line, new_item)
        if href := new_item.get_output_value('reg_href'):
            new_item.replace_value('reg_href', response.urljoin(href))
        yield new_item.load_item()


class PetrsuPagesSpider(CrawlSpider):
    name = "petrsu_pages"
    un_name = 'Петрозаводский государственный университет'
    allowed_domains = ["petrsu.ru"]
    start_urls = ["https://petrsu.ru/page/education/school/project/konferentsii-i-konkursy"]
    rules = (
        Rule(LinkExtractor(restrict_css='h4', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='ul.pagination > li.next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_xpath('conf_name', "//h1/text()")
        new_item.add_value('conf_card_href', response.url)

        for line in response.css("div.page-content").xpath(".//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
