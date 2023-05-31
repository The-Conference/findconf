from scrapy.spiders import Rule, CrawlSpider
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from ..items import ConferenceItem, ConferenceLoader
from ..utils import find_date_in_string


class CchgeuSpider(CrawlSpider):
    name = "cchgeu"
    un_name = 'Воронежский государственный технический университет'
    allowed_domains = ["cchgeu.ru"]
    start_urls = ["https://cchgeu.ru/science/info/konferentsii"]
    rules = (
        Rule(LinkExtractor(restrict_css='a.name', restrict_text='онференц'),
             callback="parse_items", follow=False),
    )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=response)

        conf_name = response.xpath("//h1/text()").get()
        new_item.add_value('conf_name', conf_name)
        new_item.add_value('conf_card_href', response.request.url)
        new_item.add_xpath('contacts', "//div[@class='news-detail']//a[contains(@href, 'mailto')]/@href")
        new_item.add_value('conf_s_desc', conf_name)

        soup = BeautifulSoup(response.text, 'lxml')
        conf_block = soup.find('div', class_='middle')
        lines = conf_block.find('div', class_='news-detail')

        out = []
        for tag in lines:
            out.append(tag.get_text(strip=True, separator='|'))
        out = '|'.join(out).split('|')
        # FIXME there are no blocks
        prev = ''
        for line in out:
            lowercase = line.lower()
            new_item.add_value('conf_desc', line)
            new_item.add_value('rinc', True if 'ринц' in lowercase else False)

            if ('состоится' in lowercase or 'открытие' in lowercase
                    or 'проведен' in lowercase or 'пройдет' in lowercase
                    or 'провод' in lowercase):
                if dates := find_date_in_string(line + prev):
                    new_item.add_value('conf_date_begin', dates[0])
                    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

            if ('заявк' in lowercase or 'принимаютс' in lowercase or 'регистрац' in lowercase or
                    'регистрир' in lowercase):
                if dates := find_date_in_string(line + prev):
                    new_item.add_value('reg_date_begin', dates[0])
                    new_item.add_value('reg_date_end', dates[1] if 1 < len(dates) else None)

            if 'организатор' in lowercase:
                new_item.add_value('org_name', line)

            if 'онлайн' in lowercase or 'трансляц' in lowercase:
                new_item.add_value('online', True)

            if 'город' in lowercase or 'адрес' in lowercase or 'место проведен' in lowercase:
                new_item.add_value('conf_address', line)
                new_item.add_value('offline', True)
            prev = lowercase

        yield new_item.load_item()
