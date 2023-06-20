import scrapy
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy_playwright.page import PageMethod

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class StankinSpider(scrapy.Spider):
    name = "stankin"
    un_name = 'Московский государственный технологический университет «СТАНКИН»'
    allowed_domains = ["stankin.ru"]
    start_urls = ["https://stankin.ru/pages/id_82/page_259",
                  "https://stankin.ru/pages/id_82/page_539"]
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_links, meta={"playwright": True})

    def parse_links(self, response):
        for link in response.css("div.ql-editor > p"):
            text = link.xpath("string(.)").get()
            href = link.xpath(".//a/@href").get()
            if 'конфер' in text.lower() and not href.lower().endswith(tuple(IGNORED_EXTENSIONS)):
                yield scrapy.Request(response.urljoin(href), callback=self.parse_items,
                                     meta={"playwright": True,
                                           "playwright_page_methods":
                                               [PageMethod("wait_for_selector", "div.ivnix-text-reader")],
                                           "link_text": text})

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_value('conf_name', response.meta.get("link_text"))

        for line in response.xpath("//div[@class='ql-container ql-snow']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)
        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(new_item.get_output_value('conf_desc'), new_item)
        yield new_item.load_item()
