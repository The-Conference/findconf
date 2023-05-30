from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_bs
from ..utils import find_date_in_string


class MsalSpider(CrawlSpider):
    name = "msal"
    un_name = 'Московский государственный юридический университет имени О.Е. Кутафина'
    allowed_domains = ["msal.ru"]
    start_urls = ["https://msal.ru/events/?arrFilter_182=34404265"
                  "&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C",
                  "https://msal.ru/events/?arrFilter_182=34404265"
                  "&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C&PAGEN_1=2"
                  ]
    rules = (
        Rule(LinkExtractor(restrict_css='a', restrict_text='Подробнее'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_id', f"{self.name}_{response.url.split('/')[-2]}")
        new_item.add_value('conf_card_href', response.url)
        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        for tag in response.css("div.text-sm.mt-2"):
            tag_txt = tag.xpath("string(.)").get().lower()
            if dates := find_date_in_string(tag_txt):
                new_item.add_value('conf_date_begin', dates[0])
                new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])
            if 'онлайн' in tag_txt or 'гибридн' in tag_txt:
                new_item.add_value('online', True)
            elif 'оффлайн' in tag_txt or 'гибридн' in tag_txt:
                new_item.add_value('offline', True)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', id='articleBody')
        lines = conf_block.find_all('p')
        for line in lines:
            new_item = default_parser_bs(line, new_item)

        new_item.add_xpath('conf_desc', "string(//div[contains(@class, 'text-block')])")
        new_item.add_css('conf_s_desc', 'div.text-block > p::text')

        yield new_item.load_item()
