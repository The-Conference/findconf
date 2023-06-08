from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class RosnouSpider(CrawlSpider):
    name = "rosnou"
    un_name = 'Российский новый университет'
    allowed_domains = ["rosnou.ru"]
    start_urls = ["https://rosnou.ru/nauka/conferences/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.article-card'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        conf_s_desc = response.xpath("string(//div[contains(@class, 'grid-item_widget-text')]/p)").get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        new_item.add_css('conf_name', "div.content-header__title-inner::text")

        for line in response.xpath("//div[@class='stage -gap-grid-inner_y_medium ']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
