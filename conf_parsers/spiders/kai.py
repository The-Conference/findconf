import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class KaiSpider(scrapy.Spider):
    name = "kai"
    un_name = 'Казанский национальный исследовательский технический университет им. А.Н. Туполева'
    allowed_domains = ["kai.ru"]
    start_urls = ["https://kai.ru/science/events"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.item', restrict_text='онференц')
        for link in link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
        soup = BeautifulSoup(response.text, 'lxml')
        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('=')[-1]}")
        new_item.add_value('conf_card_href', response.request.url)
        conf_name = response.xpath("//div[@class='title']//h1/text()").get()
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_name', conf_name)
        new_item.add_xpath('conf_s_desc', "string(//div[@class='desc'])")

        conf_block = soup.find('div', class_='journal-content-article').find('div', class_='section')
        lines = conf_block.find('div', class_='full_desc').find_all(['p', 'ul', 'ol'])

        for line in lines:
            lowercase = line.text.lower()

            if ('заявк' in lowercase or 'принимаютс' in lowercase
                    or 'регистрац' in lowercase or 'регистрир' in lowercase):
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('reg_date_begin', dates[0].date())
                    new_item.add_value('reg_date_end', dates[1].date() if 1 < len(dates) else None)

            if 'состоится' in lowercase or 'открытие' in lowercase or 'проведен' in lowercase \
                    or 'дата' in lowercase:
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('conf_date_begin', dates[0].date())
                    new_item.add_value('conf_date_end', dates[1].date() if len(dates) > 1 else dates[0].date())

            new_item.add_value('conf_desc', line.get_text(separator=" "))

            if 'регистрац' in lowercase or 'зарегистр' in lowercase or 'участия' in lowercase or 'заявк' in lowercase:
                try:
                    new_item.add_value(
                        'reg_href', line.find('a').get('href')
                        if line.find('a') and (
                                'http:' in line.find('a').get('href') or 'https:' in line.find('a').get('href')) and (
                                   '.pdf' not in line.find('a').get('href') or
                                   '.doc' not in line.find('a').get('href') or
                                   '.xls' not in line.find('a').get('href')) else None)
                except TypeError:
                    pass

            if 'организатор' in lowercase:
                new_item.add_value('org_name', line.get_text(separator=" "))

            if 'онлайн' in lowercase or 'трансляц' in lowercase or 'ссылка' in lowercase:
                new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else None)
                new_item.add_value('online', True)

            if 'место' in lowercase or 'адрес' in lowercase or 'очно' in lowercase:
                new_item.add_value('conf_address', line.text)
                new_item.add_value('offline', True)

            if ('тел.' in lowercase or 'контакт' in lowercase or 'mail' in lowercase
                    or 'почта' in lowercase or 'почты' in lowercase):
                new_item.add_value('contacts', line.text)

            if line.find('a'):
                try:
                    if 'mailto' in line.find('a').get('href'):
                        new_item.add_value('contacts', line.find('a').text)
                except TypeError:
                    pass

            new_item.add_value('rinc', True if 'ринц' in lowercase else False)

        yield new_item.load_item()
