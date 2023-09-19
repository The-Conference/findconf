from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class MsalSpider(CrawlSpider):
    name = "msal"
    un_name = 'Московский государственный юридический университет имени О.Е. Кутафина'
    allowed_domains = ["msal.ru"]
    start_urls = ["https://msal.ru/events/?arrFilter_182=34404265"
                  "&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C",
                  "https://msal.ru/events/?arrFilter_182=34404265"
                  "&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C&PAGEN_1=2"
                  ]
    rules = (
        Rule(LinkExtractor(restrict_css='a', restrict_text='Подробнее'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', 'h1::text')
        for tag in response.css("div.text-sm.mt-2"):
            tag_txt = tag.xpath("string(.)").get().lower()
            new_item = get_dates(tag_txt, new_item)
            if 'онлайн' in tag_txt or 'гибридн' in tag_txt:
                new_item.add_value('online', True)
            elif 'оффлайн' in tag_txt or 'гибридн' in tag_txt:
                new_item.add_value('offline', True)

        for line in response.xpath("//div[@id='articleBody']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)
        new_item.add_xpath('description', "string(//div[contains(@class, 'text-block')])")

        yield new_item.load_item()
