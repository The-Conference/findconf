from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class BsueduSpider(CrawlSpider):
    name = "bsuedu"
    un_name = 'Белгородский государственный национальный исследовательский университет'
    allowed_domains = ["www.bsuedu.ru"]
    start_urls = ["https://www.bsuedu.ru/bsu/science/meropr/"]
    rules = (
        Rule(LinkExtractor(restrict_css='td.mob_clear', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        new_item.add_xpath('conf_name', '//h1/text()')
        new_item.add_value('conf_card_href', response.url)

        items = response.xpath('//span')
        for item in items:
            text = item.xpath('string(.)').get()
            value = item.xpath("following-sibling::text()").get()

            if 'Дата начала' in text:
                new_item.add_value('conf_date_begin', find_date_in_string(value)[0] or None)
            if 'Дата окончания' in text:
                new_item.add_value('conf_date_end', find_date_in_string(value)[0] or None)
            if 'Срок окончания приёма заявок' in text:
                new_item.add_value('reg_date_end', find_date_in_string(value)[0] or None)
            if 'Место проведения' in text:
                new_item.add_value('conf_address', value)
            if 'Организатор' in text:
                new_item.add_value('org_name', value)
            if 'Контактная информация' in text:
                new_item.add_value('contacts', value)
            if 'Категория' in text:
                new_item.add_value('local', False if 'международн' in value.lower() else True)
            if 'Формат' in text:
                new_item.add_value('offline', True if 'очный' in value.lower()
                                                      or 'комбинир' in value.lower() else False)
                new_item.add_value('online', True if 'онлайн' in value.lower() or
                                                     'видеоконф' in value.lower() or
                                                     'комбинир' in value.lower() else False)

        text = response.xpath("string(//div[@class='news-detail'])").get()
        new_item.add_value('rinc', True if 'ринц' in text.lower() else False)
        new_item.add_xpath('conf_desc', "//div[@class='news-detail']/p[position() < 8]/text()")

        yield new_item.load_item()
