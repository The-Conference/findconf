from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class GpmuSpider(CrawlSpider):
    name = "gpmu"
    un_name = 'Санкт-Петербургский государственный педиатрический медицинский университет'
    allowed_domains = ["gpmu.org"]
    start_urls = ["https://gpmu.org/science/conference/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.catinfo_item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('conf_name', "string(//h1)")
        table_date = response.xpath("string(//div[@id='content']//td)").get()
        new_item = get_dates(table_date, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', id='content')
        lines = conf_block.find_all(['p', 'ul', 'span', 'div'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
