from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class MgpuSpider(CrawlSpider):
    name = "mgpu"
    un_name = 'Московский городской педагогический университет'
    allowed_domains = ["www.mgpu.ru"]
    start_urls = ["https://www.mgpu.ru/calendar/",
                  "https://www.mgpu.ru/calendar/?sf_paged=2"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event-modal-content', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_s_desc', conf_name)
        dates = response.xpath("string(//div[@class='event-info-date'])").get()
        new_item = get_dates(dates, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='site-content')
        lines = conf_block.find('div', class_='event-content').find_all(['p', 'ul', 'ol'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)
        yield new_item.load_item()
