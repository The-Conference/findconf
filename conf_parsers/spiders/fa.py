from urllib.parse import urlencode
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath


class FaSpider(scrapy.Spider):
    name = 'fa'
    un_name = 'Финансовый университет при Правительстве Российской Федерации'
    allowed_domains = ['fa.ru']

    def start_requests(self):
        url = 'http://www.fa.ru/org/div/oniiprs/_layouts/15/inplview.aspx?'
        querystring = {
            'List': '{278AC31B-3FAD-452A-9C38-16E6C6D269F2}',
            'View': '{5E35A48D-EEA6-4F31-BE9A-8B6E2A9ABC97}',
            'ViewCount': '84',
            'IsXslView': 'TRUE',
            'IsCSR': 'TRUE',
            'ListViewPageUrl': 'http://www.fa.ru/org/div/oniiprs/News/Forms/AllPages.aspx',
            'FilterField1': 'Category',
            'FilterValue1': 'Новости и объявления',
        }

        yield scrapy.Request(
            url=url + urlencode(querystring), method='POST', callback=self.parse_links
        )

    def parse_links(self, response):
        jsonresponse = response.json().get('Row')

        for item in jsonresponse:
            title = item.get('Title')
            link = item.get('FileRef')
            if 'конфер' in title.lower():
                yield scrapy.Request(response.urljoin(link), callback=self.parse_items)

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', 'string(//h2)')

        block = response.xpath("//div[@class='ms-rte-layoutszone-inner']")
        for line in block.xpath('.//*[self::p or self::ul or self::div]'):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
