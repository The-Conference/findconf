from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class SVfuSpider(CrawlSpider):
    name = "s-vfu"
    un_name = 'Северо-Восточный федеральный университет имени М.К. Аммосова'
    allowed_domains = ["www.s-vfu.ru"]
    start_urls = ["https://www.s-vfu.ru/universitet/nauka/sciconf/"]
    rules = (
        Rule(LinkExtractor(restrict_css='h3', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='li.bx-pag-next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "div.px-4 > h2::text")

        for line in response.xpath("//div[@class='px-4']/div//*[self::p or self::div or self::h1]"):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            dates = response.xpath("string(//div[@class='px-4']/div)").get()
            new_item = get_dates(dates, new_item)
        yield new_item.load_item()
