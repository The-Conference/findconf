from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class RzgmuSpider(CrawlSpider):
    name = "rzgmu"
    un_name = 'Рязанский государственный медицинский университет имени академика И.П. Павлова'
    allowed_domains = ["rzgmu.ru"]
    start_urls = ["https://rzgmu.ru/actions/"]
    rules = (
        Rule(LinkExtractor(restrict_css='article > a.title', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.year.current')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "main > h1::text")
        conf_s_desc = response.xpath("string(//div[@class='text']/p)").get()
        new_item.add_value('short_description', conf_s_desc)

        for line in response.xpath("//div[@class='text']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
