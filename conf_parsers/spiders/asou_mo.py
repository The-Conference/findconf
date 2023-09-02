from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class AsouMoSpider(CrawlSpider):
    name = "asou_mo"
    un_name = 'Академия социального управления'
    allowed_domains = ["asou-mo.ru"]
    start_urls = [
        "https://asou-mo.ru/events/announce/",
        # "https://asou-mo.ru/events/archive"
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='a.hentry', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_css('title', "h1.entry-title::text")
        conf_s_desc = response.xpath("//div[@class='one-news__intro-description']")
        new_item.add_value('short_description', conf_s_desc.xpath("string(.)").get())
        new_item.add_value('source_href', response.url)
        new_item.add_xpath('conf_address', "string(//div[contains(@class, 'tabs__place-info--loc')])")
        new_item.add_xpath('contacts', "string(//div[contains(@class, 'tabs__place-info--phone')])")
        new_item.add_css('reg_href', 'a.button--register::attr(href)')

        block = response.xpath(
            "//div[@class='one-news__purposes container container--news-one common-text']")
        lines = [conf_s_desc]
        lines.extend(block.xpath("./*[self::p or self::ul or self::h3]"))
        for line in lines:
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
