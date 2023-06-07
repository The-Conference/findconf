from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class MrsuSpider(CrawlSpider):
    name = "mrsu"
    un_name = 'Национальный исследовательский Мордовский государственный университет им. Н.П. Огарева'
    allowed_domains = ["mrsu.ru"]
    start_urls = ["https://mrsu.ru/ru/sci/conferences/"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.modern-page-next'), callback='parse_items', follow=True),
    )

    def parse_start_url(self, response, **kwargs):
        return self.parse_items(response)

    def parse_items(self, response):
        for card in response.css("div.b-element"):

            conf_name_item = card.css("div.head__local__institution_with_bread")
            conf_name = conf_name_item.xpath('string(.)').get()
            if 'онференц' in conf_name.lower():
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                link = conf_name_item.xpath('.//a/@href').get()
                new_item.add_value('conf_card_href', response.urljoin(link))
                new_item.add_value('conf_name', conf_name)

                for item in card.css("div.info__text"):
                    text = item.xpath('string(.)').get()
                    if 'Дата начала' in text:
                        conf_date_begin = find_date_in_string(text)[0]
                        new_item.add_value('conf_date_begin', conf_date_begin)
                    elif 'Дата окончания' in text:
                        conf_date_end = find_date_in_string(text)[0]
                        new_item.add_value('conf_date_end', conf_date_end)
                    elif 'Место проведения конференции' in text:
                        new_item.add_value('conf_address', text)
                    elif 'Организатор' in text:
                        new_item.add_value('org_name', text)
                    elif 'Исполнитель' in text or 'Контакты' in text:
                        new_item.add_value('contacts', text)
                    elif 'Статус' in text:
                        ...
                    else:
                        new_item.add_value('conf_desc', text)
                        if 'онлайн' in text:
                            new_item.add_value('online', True)
                            link = item.xpath('.//a/@href').get()
                            new_item.add_value('conf_href', link)

                conf_desc = new_item.get_collected_values('conf_desc')
                if not conf_desc:
                    new_item.add_value('conf_desc', conf_name)
                new_item.add_value('rinc', True if 'ринц' in conf_desc else False)

                yield new_item.load_item()
