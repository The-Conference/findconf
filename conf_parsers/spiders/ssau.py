from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class SsauSpider(CrawlSpider):
    name = "ssau"
    un_name = 'Самарский национальный исследовательский университет имени академика С.П. Королева'
    allowed_domains = ["ssau.ru"]
    start_urls = ["https://ssau.ru/science/rnid/conferences"]
    rules = (
        Rule(LinkExtractor(restrict_css='h5.card-title'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        new_item = get_dates(response.xpath("//div[@class='mt-3']/text()[6]").get(), new_item)

        for line in response.xpath("//article[@class='col news-content']//text()"):
            new_item = default_parser_xpath(line, new_item)

        new_item.replace_xpath('conf_address', "//div[@class='mt-3']/text()[4]")
        new_item.replace_xpath('org_name', "//div[@class='mt-3']/text()[8]")

        yield new_item.load_item()
