from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs, get_dates


class TimacadSpider(CrawlSpider):
    name = "timacad"
    un_name = 'Российский государственный аграрный университет - МСХА имени К.А. Тимирязева'
    allowed_domains = ["timacad.ru"]
    start_urls = ["https://www.timacad.ru/science/konferentsii"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.announce-item', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1.news-inner__title::text")
        conf_s_desc = response.xpath("string(//p[@class='news-inner__description'])").get()
        new_item.add_value('conf_s_desc', conf_s_desc)
        date = response.css("span.news-inner__date::text").get()
        new_item = get_dates(date, new_item)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='news-inner')
        lines = conf_block.find('div', class_='news-inner__content').find_all(['p', 'ul', 'ol'])
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        yield new_item.load_item()
