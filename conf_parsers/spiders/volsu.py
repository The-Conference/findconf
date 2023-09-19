import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class VolsuSpider(scrapy.Spider):
    name = "volsu"
    un_name = 'Волгоградский государственный университет'
    allowed_domains = ["volsu.ru"]
    start_urls = ["https://volsu.ru/archive_ad.php"]
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls.pop(), callback=self.parse_links, meta={"playwright": True})

    def parse_links(self, response):
        for card in response.css('a.card'):
            link = card.xpath('@href').get()
            title = card.xpath(".//h4/text()").get()
            if 'онференц' in title.lower():
                yield scrapy.Request(response.urljoin(link), callback=self.parse_items, meta={"playwright": True})
        next_page = response.xpath("//a[contains(text(), 'Следующая')]/@href").get()
        yield scrapy.Request(response.urljoin(next_page), callback=self.parse_links, meta={"playwright": True})

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h2::text")
        conf_s_desc = response.xpath("string(//div[@class='news-detail']/p)").get()
        new_item.add_value('short_description', conf_s_desc)

        for line in response.xpath("//div[@class='news-detail']//*[self::p or self::div or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
