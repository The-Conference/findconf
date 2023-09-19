from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class KazangmuSpider(CrawlSpider):
    name = "kazangmu"
    un_name = 'Казанский государственный медицинский университет'
    allowed_domains = ["kazangmu.ru"]
    start_urls = ["https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii"]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//section[@id='content']//a", restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='a.next')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('title', conf_name)
        new_item = get_dates(conf_name, new_item)

        for line in response.xpath("//div[@class='content clearfix']/*"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
