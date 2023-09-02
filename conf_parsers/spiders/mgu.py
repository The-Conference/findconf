import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class MguSpider(scrapy.Spider):
    name = "mgu"
    un_name = 'Московский государственный университет имени М.В.Ломоносова'
    allowed_domains = ["msu.ru"]
    start_urls = ["https://www.msu.ru/science/allevents.html"]

    def parse(self, response, **kwargs):
        for card in response.xpath("//div[@class='news-list-item news-list-item-conf']"):
            type_and_date = card.xpath("string(.//div[@class='news-list-item-conf-daterange'])").get()
            if 'конфер' in type_and_date.lower():
                link = card.xpath(".//a/@href").get()
                yield scrapy.Request(link, callback=self.parse_items, meta={
                    'type_and_date': type_and_date,
                })

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1)")
        new_item.add_xpath('short_description', "string(//p[@class='event__description'])")
        regs = response.xpath("//div[@class='col-sm-4 event-table__cell'][last()]")
        new_item = default_parser_xpath(regs, new_item)
        new_item = get_dates(response.meta.get('type_and_date'), new_item)
        new_item.replace_value('description', '')

        for block in response.xpath("//div[@class='block__content']"):
            title = block.xpath("string(./h2)").get()
            if not title:
                for line in block.xpath("./div[@class='event__text']/*[self::p or self::div or self::ul]"):
                    new_item = default_parser_xpath(line, new_item)
            if title == 'Контактная информация':
                new_item.add_value('contacts', block.xpath("string(./div)").get())
        yield new_item.load_item()
