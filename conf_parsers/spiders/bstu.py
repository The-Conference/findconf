import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates


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
                new_item.add_value('title', conf_name)
                new_item.add_value('description', conf_name)
                href = link.css("a::attr(href)").get() or None
                if href:
                    new_item.add_value('source_href', response.urljoin(href))
                dates_str = link.css("strong::text")[-1].get()
                new_item = get_dates(dates_str, new_item)

                yield new_item.load_item()

