from datetime import datetime
from scrapy.linkextractors import IGNORED_EXTENSIONS
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class EtuSpider(scrapy.Spider):
    name = "etu"
    un_name = 'Санкт-Петербургский государственный электротехнический университет «ЛЭТИ» имени В. И. Ульянова (Ленина)'
    allowed_domains = ["etu.ru"]
    start_urls = ["https://etu.ru/ru/nauchnaya-i-innovacionnaya-deyatelnost/konferencii-seminary-vystavki/v-spbgetu"]

    def parse(self, response, **kwargs):
        current_year = str(datetime.now().year)
        table = response.xpath(f"//table[preceding::h2[1][contains(text(), {current_year})]]")
        for row in table.xpath(".//tr"):
            cols = row.xpath(".//td")
            try:
                dates = cols[0].xpath("string(.)").get() + current_year
                links = cols[1].xpath(".//a")
                contacts = cols[2].xpath("string(.)").get()
            except IndexError:
                continue
            for link in links:
                url = link.xpath("./@href").get()
                title = link.xpath("./text()").get()
                if not url.endswith(tuple(IGNORED_EXTENSIONS)) and title and 'конф' in title.lower():
                    yield scrapy.Request(response.urljoin(url), callback=self.parse_items,
                                         meta={'dates': dates,
                                               'title': title,
                                               'contacts': contacts})

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_value('title', response.meta.get('title'))
        new_item = get_dates(response.meta.get('dates'), new_item)
        new_item.add_css('conf_address', "div.location::text")

        for line in response.xpath("//div[@id='content']//*[self::p or self::li]"):
            new_item = default_parser_xpath(line, new_item)

        new_item.replace_value('contacts', response.meta.get('contacts'))
        yield new_item.load_item()
