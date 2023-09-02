import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class MietSpider(scrapy.Spider):
    name = "miet"
    un_name = 'Национальный исследовательский университет «МИЭТ»'
    allowed_domains = ["miet.ru"]
    start_urls = ["https://miet.ru/"]

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls.pop(), callback=self.parse, meta={"playwright": True})

    def parse(self, response, **kwargs):
        main_page = LinkExtractor(restrict_css='div.header-menu__toggable-item__list-item',
                                  restrict_text='Конференции и семинары')
        url = main_page.extract_links(response)[0].url
        yield scrapy.Request(url, callback=self.get_links, meta={"playwright": True})

    def get_links(self, response):
        link_extractor = LinkExtractor(restrict_css='a.site-sidebar__item-link',
                                       restrict_text='^((?!Архив).)*$')
        links = [i.url for i in link_extractor.extract_links(response)]
        links.append(response.url)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_items, meta={"playwright": True})

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "//h2/text()")

        for line in response.xpath("//div[@class='info-content']//*[self::p]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
