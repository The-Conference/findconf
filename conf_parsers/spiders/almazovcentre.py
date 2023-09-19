from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class AlmazovcentreSpider(CrawlSpider):
    name = "almazovcentre"
    un_name = 'ФГБУ «НМИЦ им. В. А. Алмазова» Минздрава России'
    allowed_domains = ["www.almazovcentre.ru"]
    start_urls = ["http://www.almazovcentre.ru/?cat=5"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.entry-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        conf_name = response.css("a.entry-title::text").get()
        new_item.add_value('title', conf_name)
        new_item.add_value('source_href', response.url)
        new_item.add_xpath('reg_href', "//div[@class='personal']/a[contains(.,'Регистрация')]/@href")
        new_item = get_dates(conf_name, new_item)

        for line in response.xpath("//div[@class='entry fix']/*[self::p or self::div[not(@class)]]"):
            new_item = default_parser_xpath(line, new_item)
        new_item.replace_xpath('conf_address', "string(//div[@class='information'])")

        yield new_item.load_item()
