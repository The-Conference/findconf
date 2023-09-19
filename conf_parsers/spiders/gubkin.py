from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string
from ..parsing import get_dates


class GubkinSpider(CrawlSpider):
    name = "gubkin"
    un_name = 'Российский государственный университет нефти и газа ' \
              '(национальный исследовательский университет) имени И.М. Губкина'
    allowed_domains = ["conf.gubkin.ru"]
    start_urls = ["https://conf.gubkin.ru/conferences/"]
    rules = (
        Rule(LinkExtractor(restrict_css='td.name', restrict_text='онференц', attrs=('data-short',)),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        conf_name = response.xpath("string(//div[@class='modal-header'])").get()
        new_item.add_value('title', conf_name)
        new_item.add_value('source_href', response.url)
        new_item.add_value('short_description', conf_name)
        new_item.add_css('description', "div.modal-body:not(.ul)::text")

        _dates = response.xpath("string(//li[@class='date-short'])").get()
        new_item = get_dates(_dates, new_item)

        _dates = response.xpath("string(//li[@class='date-short'][2])").get()
        if dates := find_date_in_string(_dates):
            new_item.add_value('reg_date_end', dates[0])
        new_item.add_xpath('org_name', "string(//li[@class='host-short'])")
        new_item.add_xpath('conf_address', "string(//li[@class='geo-short'])")
        link_extractor = LinkExtractor(restrict_css='li.www-short')
        _links = link_extractor.extract_links(response)
        new_item.add_value('conf_href', _links[0].url if _links else None)
        yield new_item.load_item()
