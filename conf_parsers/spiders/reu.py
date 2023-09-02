from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class ReuSpider(CrawlSpider):
    name = "reu"
    un_name = 'Российский экономический университет имени Г.В. Плеханова'
    allowed_domains = ["рэу.рф", "xn--p1ag3a.xn--p1ai", "rea.ru"]
    start_urls = ["https://рэу.рф/science/direktsiya-po-nauke-i-innovatsiyam/orgnirupr/otdel_nauchnyh_meropriyatij/"
                  "informatsiya_o_nauchnykh_meropriyatiyakh/aktualnye_nauchnye_meropriyatiya"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.event__block-text--data-link'), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_css('title', "h1::text")
        new_item.add_css('title', "title::text")
        dates = response.css("div.page-event-date::text").get() or \
                response.xpath("string(//div[@class='mydate'])").get()
        new_item = get_dates(dates, new_item)

        block = response.xpath("//div[@class='page-event-text']") or response.xpath("//div[@class='wrapper about']")
        for line in block.xpath(".//text()"):
            new_item = default_parser_xpath(line, new_item)

        for block in response.css("div.page-event-info-col > div"):
            title = block.css("div.page-event-info-name::text").get().lower()
            data = block.css("div.page-event-info-title::text").get()
            if 'организатор' in title:
                new_item.add_value('org_name', data)
            elif 'контакты' in title:
                new_item.add_value('contacts', data)
            elif 'место' in title:
                new_item.add_value('conf_address', data)

        yield new_item.load_item()
