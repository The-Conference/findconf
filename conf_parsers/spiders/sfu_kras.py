import scrapy
import html

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class SfuKrasSpider(scrapy.Spider):
    name = "sfu-kras"
    un_name = 'Сибирский федеральный университет'
    allowed_domains = ["conf.sfu-kras.ru"]
    start_urls = ["https://conf.sfu-kras.ru/"]

    def parse(self, response, **kwargs):
        for link in response.css('div.listItem'):
            href = link.css('a::attr(href)').get()
            if 'онференц' in link.xpath('string(.)').get():
                yield scrapy.Request(response.urljoin(href), callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//h2)")
        new_item.add_xpath('short_description', "string(//h4)")

        for line in response.xpath("//div[@class='confs-container']//*[self::div[@class='row']]"):
            new_item = default_parser_xpath(line, new_item)
            lower = line.xpath("string(.)").get().lower()
            if 'сайт' in lower:
                href = line.xpath(".//a/@href").get()
                new_item.add_value('conf_href', href)
            if 'mail' in lower:
                encoded = line.xpath(".//script/text()").get()
                if decoded := self.decode_email(encoded):
                    new_item.add_value('contacts', decoded)
        if href := new_item.get_output_value('reg_href'):
            new_item.replace_value('reg_href', href)
        yield new_item.load_item()

    @staticmethod
    def decode_email(encoded: str) -> str:
        prep = encoded.split('"')[1::2][0].replace("'+'", "")
        decode = html.unescape(prep)
        decode = decode.replace('mailto:', '')
        return decode
