import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


class MpeiSpider(scrapy.Spider):
    name = "mpei"
    un_name = 'Национальный исследовательский университет «МЭИ»'
    allowed_domains = ["mpei.ru"]
    start_urls = ["https://mpei.ru/Science/ScientificEvents/Pages/default.aspx"]

    def parse(self, response, **kwargs):
        for card in response.css("div.event-card"):
            new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

            conf_name = card.css("div:not([class])::text").get()
            new_item.add_value('conf_name', conf_name)
            new_item.add_value('conf_card_href', response.url)
            _dates = card.xpath("string(.//div[@class='event-date'])").get()
            new_item = get_dates(_dates, new_item, is_vague=True)
            new_item.add_value('conf_desc', conf_name)
            new_item.add_value('conf_s_desc', conf_name)

            for line in card.xpath(".//div[@class='event-info']"):
                text = line.xpath("./text()").get()
                if 'addr' in line.get():
                    field = 'conf_address'
                elif 'site' in line.get():
                    field = 'conf_href'
                    text = line.css("a::attr(href)").get()
                else:
                    field = 'contacts'
                new_item.add_value(field, text)

            yield new_item.load_item()
