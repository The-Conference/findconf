from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class DonstuSpider(CrawlSpider):
    name = "donstu"
    un_name = 'Донской государственный технический университет'
    allowed_domains = ["donstu.ru"]
    start_urls = ["https://donstu.ru/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event-box', allow='konfer'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("//div[@class='title']/text()").get()
        new_item.add_value('conf_name', conf_name)
        conf_s_desc = response.xpath("//div[@class='desc']/text()").get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        new_item.add_value('conf_card_href', response.request.url)
        conf_date_begin = response.xpath("string(//div[@class='event-date'])").get()
        new_item = get_dates(conf_date_begin, new_item)
        conf_address = response.xpath("string(//div[@class='event-location'])").get()
        online = True if 'онлайн' in conf_address.lower() else False
        offline = not online
        new_item.add_value('online', online)
        new_item.add_value('offline', offline)
        if offline:
            new_item.add_value('conf_address', conf_address)

        soup = BeautifulSoup(response.text, 'lxml')
        main_containers = soup.find('div', class_='event-container')
        lines = main_containers.find('div', class_='text-block')
        if lines.find('p'):
            lines = lines.find_all(['p', 'ul'])

        for line in lines:
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
