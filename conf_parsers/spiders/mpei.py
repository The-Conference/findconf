import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string, parse_vague_dates


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
            dates = find_date_in_string(_dates)
            if not dates:
                dates = parse_vague_dates(_dates)
            conf_date_begin = dates[0] or ''
            conf_date_end = dates[1] if len(dates) > 1 else dates[0]
            new_item.add_value('conf_date_begin', conf_date_begin)
            new_item.add_value('conf_date_end', conf_date_end)
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
