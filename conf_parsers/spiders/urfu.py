import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_plain_text


class UrfuSpider(scrapy.Spider):
    name = "urfu"
    un_name = 'Уральский федеральный университет имени первого Президента России Б.Н. Ельцина'
    allowed_domains = ["urfu.ru"]
    start_urls = ["https://urfu.ru/ru/science/konferencii/"]

    def parse(self, response, **kwargs):
        for row in response.xpath("//table[@class='ce-table']//tr"):
            td = row.xpath(".//td")
            try:
                conf_name = td[0].xpath("string(.)").get()
                dates = td[1].xpath("string(.)").get()
                link = td[2].xpath(".//a[contains(., 'меропр')]/@href").get()
            except IndexError:
                continue

            new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

            new_item.add_value('conf_name', conf_name)
            new_item.add_value('conf_card_href', response.url)
            new_item.add_value('conf_href', link)
            new_item = get_dates(self.prep_dates(dates), new_item)
            new_item = parse_plain_text(conf_name, new_item)
            yield new_item.load_item()

    def prep_dates(self, string: str):
        """Incorporating this edge case into the main regexp proved
        too difficult. In over 60 parsers, this is the only time this
        notation is used, so for now it's not worth the trouble.

        Problematic format: 29.05-02.06.2023
        """
        s = string.split('-')
        if len(s[0]) > 2:
            year = s[1].split('.')[-1]
            return f'{s[0]}.{year} / {s[1]}'
        else:
            return string
