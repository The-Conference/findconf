from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class SzgmuSpider(CrawlSpider):
    name = "szgmu"
    un_name = 'Северо-Западный государственный медицинский университет имени И.И. Мечникова'
    allowed_domains = ["szgmu.ru"]
    start_urls = ["https://szgmu.ru/modules/ev/index.php"]
    rules = (
        Rule(LinkExtractor(restrict_css='span#next-month'), callback='parse_items', follow=True),
    )
    custom_settings = {
        "DEPTH_LIMIT": 6
    }

    def parse_start_url(self, response, **kwargs):
        return self.parse_items(response)

    def parse_items(self, response):
        for conf in response.css('div.event-item-content'):
            conf_name = conf.css('h1::text').get()
            if 'онференц' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
                new_item.add_value('source_href', response.url)
                new_item.add_value('title', conf_name)
                new_item.add_value('description', conf_name)
                dates_select = conf.xpath("string(//div[@class='meta-panel'])").get()
                new_item = get_dates(dates_select, new_item)

                yield new_item.load_item()
