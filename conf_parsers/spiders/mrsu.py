import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class MrsuSpider(scrapy.Spider):
    name = "mrsu"
    un_name = 'Национальный исследовательский Мордовский государственный университет им. Н.П. Огарева'
    allowed_domains = ["mrsu.ru"]
    start_urls = ["https://mrsu.ru/ru/sci/conferences/?PAGEN_1=3"]

    def parse(self, response, **kwargs):
        for card in response.css("div.b-element"):

            conf_name_item = card.css("div.head__local__institution_with_bread")
            conf_name = conf_name_item.xpath('string(.)').get()
            if 'онференц' in conf_name.lower():
                conf_date_begin = conf_date_end = ''
                new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

                link = conf_name_item.xpath('.//a/@href').get()
                new_item.add_value('conf_card_href', response.urljoin(link))
                new_item.add_value('conf_name', conf_name)

                for item in card.css("div.info__text"):
                    text = item.xpath('string(.)').get()
                    if 'Дата начала' in text:
                        conf_date_begin = find_date_in_string(text)[0]
                    elif 'Дата окончания' in text:
                        conf_date_end = find_date_in_string(text)[0]
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
                new_item.add_value('conf_date_begin', conf_date_begin)
                new_item.add_value('conf_date_end', conf_date_end if conf_date_end else conf_date_begin)
                new_item.add_value('rinc', True if 'ринц' in conf_desc else False)

                yield new_item.load_item()

