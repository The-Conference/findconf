from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class MgppuSpider(CrawlSpider):
    name = "mgppu"
    un_name = 'Московский государственный психолого-педагогический университет'
    allowed_domains = ["mgppu.ru"]
    start_urls = ["https://mgppu.ru/events?searchStr=&eventtype_conference=y"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.new-link', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        dates = response.xpath("//time/text()").get()
        new_item = get_dates(dates, new_item)
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='page container').find('div', class_='col-sm-12')
        lines = conf_block.find_all(['p', 'ul', 'ol'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
