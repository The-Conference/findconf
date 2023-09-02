from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MftiSpider(CrawlSpider):
    name = "mfti"
    un_name = 'Московский физико-технический институт (национальный исследовательский университет)'
    allowed_domains = ["mipt.ru"]
    start_urls = ["https://mipt.ru/news/?t=конференция,Приоритет2030"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.title.link', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")

        for line in response.xpath("//div[@class='post-contents']/*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
