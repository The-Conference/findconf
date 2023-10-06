import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class SpbgasuSpider(scrapy.Spider):
    name = 'spbgasu'
    un_name = 'Санкт-Петербургский государственный архитектурно-строительный университет'
    allowed_domains = ['spbgasu.ru']
    start_urls = ['https://www.spbgasu.ru/science/konferentsii-i-seminary/']

    def parse(self, response, **kwargs):
        for row in response.css('tr'):
            cells = row.css('td')
            if len(cells) > 1:
                href = cells[1].css('a::attr(href)').get()
                title = cells[1].xpath('string(.)').get()
                contacts = cells[-1].xpath('string(.)').get()
                if href and 'онференц' in title.lower():
                    yield scrapy.Request(
                        response.urljoin(href),
                        callback=self.parse_items,
                        meta={'contacts': contacts},
                    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h1[@class='page-head__title'])")
        conf_s_desc = response.xpath("string(//p[contains(@class, 'page-head__subtitle')])").get()
        new_item.add_value('short_description', conf_s_desc)
        new_item = get_dates(conf_s_desc, new_item, is_vague=True)

        for line in response.xpath("//main/*[@class='app-section _small-gutter']"):
            new_item = default_parser_xpath(line, new_item)
        new_item.replace_value('contacts', response.meta.get('contacts'))
        yield new_item.load_item()
