from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class RanepaSpiderIIM(CrawlSpider):
    name = "ranepa-iim"
    un_name = 'Институт отраслевого менеджмента РАНХиГС'
    allowed_domains = ["iim.ranepa.ru"]
    start_urls = ["https://iim.ranepa.ru/about/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.specialty__item'), callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        desc = response.xpath("string(//div[@class='conf-intro__headline'])").get()
        if 'онференц' in desc.lower():
            new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

            new_item.add_value('conf_card_href', response.url)
            new_item.add_css('conf_name', "h1::text")
            new_item.add_value('conf_s_desc', desc)
            dates = response.xpath("string(//div[@class='conf-intro__date'])").get()
            new_item = get_dates(dates, new_item)
            new_item.add_css('conf_address', "div.contacts__left > div.contact::text")

            for line in response.xpath("//div[@class='section-indent bgc--default']//*[self::p or self::ul]"):
                new_item = default_parser_xpath(line, new_item)
            yield new_item.load_item()


class RanepaSpiderIURR(CrawlSpider):
    name = "ranepa-iurr"
    un_name = 'Институт управления и регионального развития РАНХиГС'
    allowed_domains = ["iurr.ranepa.ru"]
    start_urls = ["http://iurr.ranepa.ru/category/news/anounces/"]
    rules = (
        Rule(LinkExtractor(restrict_css='article.single-news-article', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        conf_name = response.css("h1::text").get()
        new_item.add_value('conf_name', conf_name)
        new_item = get_dates(conf_name, new_item)

        for line in response.xpath("//div[@class='thecontent']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)
        desc = response.xpath("//div[@class='thecontent']//*[self::p][position() < 10]//text()").getall()
        new_item.replace_value('conf_desc', desc)
        yield new_item.load_item()


class RanepaSpiderIGSU(CrawlSpider):
    name = "ranepa-igsu"
    un_name = 'Институт государственной службы и управления РАНХиГС'
    allowed_domains = ["igsu.ranepa.ru"]
    start_urls = ["https://igsu.ranepa.ru/science/confs/"]
    rules = (
        Rule(LinkExtractor(restrict_css='h2.entry-title', restrict_text='онференц'),
             callback="parse_items", follow=False),
        Rule(LinkExtractor(restrict_css='div.pull-right')),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")

        text_block = response.xpath("//div[@class='et_pb_text_inner']")
        for line in text_block.xpath("./*[self::p or self::ul or starts-with(name(),'h')]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()


class RanepaSpiderGSCM(CrawlSpider):
    name = "ranepa-gscm"
    un_name = 'Институт государственной службы и управления РАНХиГС'
    allowed_domains = ["gscm.ranepa.ru"]
    start_urls = ["https://gscm.ranepa.ru/about/events/"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.activity-block', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")

        for line in response.xpath("//div[@class='news-detail__text']//*[self::p or self::ul]"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()


class RanepaSpiderION(CrawlSpider):
    name = "ranepa-ion"
    un_name = 'Институт общественных наук РАНХиГС'
    allowed_domains = ["ion.ranepa.ru"]
    start_urls = ["https://ion.ranepa.ru/announcement/f/event_type-21/"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.b-txt'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('conf_card_href', response.url)
        new_item.add_css('conf_name', "h1::text")
        new_item.add_xpath('conf_s_desc', "string(//div[@class='b-program-fin']/p)")

        # no tags. Splitting text by <br>
        for line in response.xpath("//article/*[not(div)]//text()"):
            new_item = default_parser_xpath(line, new_item)

        yield new_item.load_item()
