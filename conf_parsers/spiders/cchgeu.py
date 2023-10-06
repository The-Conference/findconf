from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, default_parser_xpath


class CchgeuSpider(CrawlSpider):
    name = 'cchgeu'
    un_name = 'Воронежский государственный технический университет'
    allowed_domains = ['cchgeu.ru']
    start_urls = ['https://cchgeu.ru/science/info/konferentsii']
    rules = (
        Rule(
            LinkExtractor(restrict_css='a.name', restrict_text='онференц'),
            callback='parse_items',
            follow=False,
        ),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        conf_name = response.xpath('//h1/text()').get()
        new_item.add_value('title', conf_name)
        new_item.add_value('source_href', response.url)
        new_item.add_xpath(
            'contacts', "//div[@class='news-detail']//a[contains(@href, 'mailto')]/@href"
        )

        text = response.xpath("//div[@class='news-detail']/div[not(@class or @style)]")
        # no tags. Splitting text by <br>
        for line in text.xpath('text()'):
            new_item = default_parser_xpath(line, new_item)

        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(text.xpath('string(.)').get(), new_item)

        yield new_item.load_item()
