from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


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
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("string(//div[@class='modal-header'])").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_value('conf_s_desc', conf_name)
        new_item.add_css('conf_desc', "div.modal-body:not(.ul)::text")

        _dates = response.xpath("string(//li[@class='date-short'])").get()
        if dates := find_date_in_string(_dates):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if 1 < len(dates) else dates[0])

        _dates = response.xpath("string(//li[@class='date-short'][2])").get()
        if dates := find_date_in_string(_dates):
            new_item.add_value('reg_date_end', dates[0])
        new_item.add_xpath('org_name', "string(//li[@class='host-short'])")
        new_item.add_xpath('conf_address', "string(//li[@class='geo-short'])")
        link_extractor = LinkExtractor(restrict_css='li.www-short')
        _links = link_extractor.extract_links(response)
        new_item.add_value('conf_href', _links[0].url if _links else None)
        yield new_item.load_item()
