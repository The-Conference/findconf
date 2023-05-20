import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class AlmazovcentreSpider(scrapy.Spider):
    name = "almazovcentre"
    un_name = 'ФГБУ «НМИЦ им. В. А. Алмазова» Минздрава России'
    allowed_domains = ["www.almazovcentre.ru"]
    start_urls = ["http://www.almazovcentre.ru/?cat=5"]

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor(restrict_css='a.entry-title', restrict_text='онференц')
        links = link_extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_items)

    def parse_items(self, response, **kwargs):
        new_item = ConferenceLoader(item=ConferenceItem())

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='entry fix')

        new_item.add_value('conf_id', f"{self.name}_{response.request.url.split('=')[-1]}")
        conf_name = soup.find('article').find('div', class_='title').find('a').text
        new_item.add_value('local', False if 'международн' in conf_name.lower() else True)
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_card_href', response.request.url)

        if side_block := conf_block.find('div', class_='personal'):
            for ref in side_block.find_all('a'):
                new_item.add_value('reg_href', ref.get('href') if 'регистрация' in ref.text.lower() else None)

        if dates := find_date_in_string(conf_name):
            new_item.add_value('conf_date_begin', dates[0].date())
            new_item.add_value('conf_date_end', dates[1].date() if len(dates) > 1 else dates[0].date())

        lines = conf_block.find_all(['p', 'div'])
        for line in lines:
            lowercase = line.text.lower()
            new_item.add_value('conf_desc', line.get_text(separator=" "))

            if ('заявк' in lowercase or 'принимаютс' in lowercase or 'участи' in lowercase
                or 'регистрац' in lowercase or 'регистрир' in lowercase):
                if dates := find_date_in_string(lowercase):
                    new_item.add_value('reg_date_begin', dates[0].date())
                    new_item.add_value('reg_date_end', dates[1].date() if 1 < len(dates) else None)

            if ('онлайн' in lowercase or 'трансляц' in lowercase or
                               'на платформе' in lowercase or 'дистанционном' in lowercase):
                new_item.add_value('online', True)
                new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else 'отсутствует')

            if ('место' in lowercase or 'места' in lowercase or
                                'ждем вас в' in lowercase or 'адрес' in lowercase):
                new_item.add_value('offline', True)
                new_item.add_value('conf_address', line.get_text(separator=" "))

            if 'организатор' in lowercase:
                new_item.add_value('org_name', line.get_text(separator=" "))

            if ('тел.' in lowercase or 'контакт' in lowercase or 'mail' in lowercase
                    or 'почта' in lowercase or 'почты' in lowercase):
                new_item.add_value('contacts', line.text)

            if line.find('a') and 'mailto' in line.find('a').get('href'):
                new_item.add_value('contacts', line.find('a').text)

            new_item.add_value('rinc', True if 'ринц' in lowercase else False)
        yield new_item.load_item()
