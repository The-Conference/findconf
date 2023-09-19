from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class VavtSpider(CrawlSpider):
    name = "vavt"
    un_name = 'Всероссийская академия внешней торговли Министерства экономического развития Российской Федерации'
    allowed_domains = ["www.vavt.ru"]  # Keep an eye on subdomains, ignoring for now
    start_urls = ["https://www.vavt.ru/science/site/konf_vavt"]
    rules = (
        Rule(LinkExtractor(restrict_css='table.list td.list_txt'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_value('title', response.meta.get("link_text"))
        new_item.add_css('short_description', "h1::text")

        for line in response.xpath("//div[@id='content1']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('title'), new_item)

        yield new_item.load_item()
