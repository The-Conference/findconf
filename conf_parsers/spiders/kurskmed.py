from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class KurskmedSpider(CrawlSpider):
    name = "kurskmed"
    un_name = 'Курский государственный медицинский университет'
    allowed_domains = ["kurskmed.com"]
    start_urls = ["https://kurskmed.com/department/KSMU_announcements_events/news"]
    rules = (
        Rule(LinkExtractor(restrict_css='div.news_list', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', "string(//div[@class='detail_title']/div[@class='detail_title'])")

        for line in response.xpath("//div[@class='text_news']/*"):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            # This date is wrong, but it's better than no date.
            dates = response.css("div.date::text").get()
            new_item = get_dates(dates, new_item)

        yield new_item.load_item()
