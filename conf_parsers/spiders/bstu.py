import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class BstuSpider(scrapy.Spider):
    name = "bstu"
    un_name = 'БГТУ им. В.Г. Шухова'
    allowed_domains = ["conf.bstu.ru"]
    start_urls = ["https://conf.bstu.ru/conf_bstu"]

    def parse(self, response, **kwargs):
        links = response.xpath("//article[@class='content']//li")

        for link in links:
            conf_name = link.xpath("string(.)").get()
            if 'конференц' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
                new_item.add_value('conf_name', conf_name)
                href = link.css("a::attr(href)").get() or None
                if href:
                    new_item.add_value('conf_card_href', response.urljoin(href))
                dates_str = link.css("strong::text")[-1].get()
                if dates := find_date_in_string(dates_str):
                    new_item.add_value('conf_date_begin', dates[0])
                    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

                yield new_item.load_item()

