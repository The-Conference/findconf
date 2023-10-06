import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_playwright.page import PageMethod

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MgimoSpider(scrapy.Spider):
    name = 'mgimo'
    un_name = 'МГИМО МИД России'
    allowed_domains = ['mgimo.ru']
    start_urls = ['https://mgimo.ru/about/news/conferences/']
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        }
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mgimo.ru/science/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
    }

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls.pop(),
            callback=self.parse_links,
            headers=self.headers,
            meta={
                'playwright': True,
                'playwright_page_methods': [PageMethod('wait_for_selector', 'a.title')],
            },
        )

    def parse_links(self, response):
        link_extractor = LinkExtractor(restrict_css='a.title')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(
                link.url,
                callback=self.parse_items,
                headers=self.headers,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [PageMethod('wait_for_selector', 'h1')],
                },
            )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', '//h1/text()')

        for line in response.xpath(
            "//div[@class='templ01__text-container post']/*[self::p or self::ul]"
        ):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
