import scrapy

from ..items import ConferenceLoader, GrantItem
from ..utils import find_date_in_string


class RNFGrantSpider(scrapy.Spider):
    name = 'grant_rnf'
    un_name = 'Российский научный фонд'
    allowed_domains = ['rscf.ru']
    start_urls = ['https://rscf.ru/contests/?status=acceptance']

    def parse(self, response, **kwargs):
        for row in response.css('div#classification-table > div.classification-table-row'):
            new_item = ConferenceLoader(item=GrantItem(), selector=row, response=response)
            new_item.add_value('source_href', response.url)
            new_item.add_css('title', 'div.contest-name::text')
            new_item.add_css('description', 'div.contest-name::text')
            if date := row.css('div.contest-date > span.contest-success::text').get():
                new_item.add_value('reg_date_end', find_date_in_string(date)[0])
            new_item.add_css('reg_href', 'div.contest-date a::attr(href)')
            yield new_item.load_item()
