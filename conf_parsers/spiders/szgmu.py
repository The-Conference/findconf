from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


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
                new_item.add_value('conf_card_href', response.url)
                new_item.add_value('conf_name', conf_name)
                new_item.add_value('conf_s_desc', conf_name)
                new_item.add_value('conf_desc', conf_name)
                dates_select = conf.xpath("string(//div[@class='meta-panel'])").get()
                if dates := find_date_in_string(dates_select):
                    new_item.add_value('conf_date_begin', dates[0])
                    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
                yield new_item.load_item()
