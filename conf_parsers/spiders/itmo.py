from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class ItmoSpider(CrawlSpider):
    name = "itmo"
    un_name = 'Национальный исследовательский университет ИТМО'
    allowed_domains = ["news.itmo.ru"]
    start_urls = ["https://news.itmo.ru/ru/events/?order=upcoming&types=2",
                  # "https://news.itmo.ru/ru/events/?order=past&types=2",
                  ]
    rules = (
        Rule(LinkExtractor(restrict_css="div.weeklyevents.sand a"),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        dates = response.css("div.summary time::text").get()
        new_item = get_dates(dates, new_item)
        new_item.add_css('conf_address', "div.summary li > a > p::text")

        for line in response.xpath("//div[@class='content js-mediator-article']/*"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
