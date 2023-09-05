from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_conf


class TpuSpider(CrawlSpider):
    name = "tpu"
    un_name = 'Томский технологический институт'
    allowed_domains = ["tpu.ru"]
    start_urls = ["https://portal.tpu.ru/science/konf?m=0"]
    rules = (
        Rule(LinkExtractor(restrict_css='span.normal.c-pages', restrict_text='>>'),
             callback="parse_items", follow=True),
    )

    def parse_start_url(self, response, **kwargs):
        return self.parse_items(response)

    def parse_items(self, response):
        for row in response.xpath("//table[@class='little']//tr"):
            td = row.xpath(".//td")
            try:
                conf_name = td[0].xpath("string(.)").get()
                dates = td[1].xpath("string(.)").get()
                contacts = td[2].xpath("text()")
                link = td[3].xpath(".//a[contains(., 'меропр')]/@href").get()
            except IndexError:
                continue

            if 'конфер' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                new_item.add_value('title', conf_name)
                new_item.add_value('source_href', response.url)
                new_item.add_value('conf_href', link)
                new_item = get_dates(dates, new_item)
                new_item = parse_conf(conf_name, new_item)
                new_item.add_value('conf_address', contacts.get())
                for i in contacts[1:]:
                    new_item.add_value('contacts', i.get())
                yield new_item.load_item()
