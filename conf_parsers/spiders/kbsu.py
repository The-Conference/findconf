from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class KbsuSpider(CrawlSpider):
    name = "kbsu"
    un_name = 'Кабардино-Балкарский государственный университет им. Х. М. Бербекова'
    allowed_domains = ["kbsu.ru"]
    start_urls = ["https://kbsu.ru/nauchnye-konferencii/"]
    rules = (
        Rule(LinkExtractor(restrict_css='td > a', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        conf_name = response.meta.get('link_text')
        new_item.add_value('title', conf_name)
        new_item = get_dates(response.xpath("//h1/text()").get(), new_item)

        for line in response.xpath("//div[@class='single__content content ']//*[self::p or self::ul or self::ol]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
