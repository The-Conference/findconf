from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class MuctrSpider(CrawlSpider):
    name = "muctr"
    un_name = 'Российский химико-технологический университет имени Д.И. Менделеева'
    allowed_domains = ["muctr.ru"]
    start_urls = ["https://www.muctr.ru/notifies/konferentsii/"]
    rules = (
        Rule(LinkExtractor(restrict_css="div.news-item-text"),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_xpath('conf_name', "string(//div[@class='content-page-title'])")

        for line in response.xpath("//div[@class='news-item-text clearfix']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)

        # TODO remove this when sentencer is done.
        new_item.replace_value('conf_date_end', '')
        dates = response.css("div.news-item-date").xpath("string(.)").get()
        new_item = get_dates(dates, new_item)

        yield new_item.load_item()
