from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs


class KaiSpider(CrawlSpider):
    name = "kai"
    un_name = 'Казанский национальный исследовательский технический университет им. А.Н. Туполева'
    allowed_domains = ["kai.ru"]
    start_urls = ["https://kai.ru/science/events"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('conf_name', "//div[@class='title']//h1/text()")
        new_item.add_xpath('conf_s_desc', "string(//div[@class='desc'])")

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='journal-content-article').find('div', class_='section')
        lines = conf_block.find('div', class_='full_desc').find_all(['p', 'ul', 'ol'])

        for line in lines:
            new_item.add_value('conf_s_desc', line.get_text(separator=" "))
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
