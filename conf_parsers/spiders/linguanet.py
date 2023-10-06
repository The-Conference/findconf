import scrapy
from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class LinguanetSpider(scrapy.Spider):
    name = 'linguanet'
    un_name = 'Московский государственный лингвистический университет'
    allowed_domains = ['www.linguanet.ru']
    start_urls = ['https://www.linguanet.ru/science/konferentsii-i-seminary/']

    def parse(self, response, **kwargs):
        for line in response.css('div.page.col-xs-12.col-sm-9').xpath('./*[self::div or self::p]'):
            conf_name = line.css('::text')[1].get()
            full_text = line.xpath('string(.)').get().lower()
            if 'конфер' in full_text:
                new_item = ConferenceLoader(item=ConferenceItem(), response=response)
                new_item.add_value('title', conf_name)
                new_item.add_value('description', conf_name)

                new_item = get_dates(full_text, new_item)
                date = new_item.get_output_value('conf_date_begin')
                if date and date < self.settings.get('FILTER_DATE'):
                    break

                for i in line.css('a'):
                    link = i.css('::attr(href)').get()
                    text = i.get().lower()
                    if 'регистрац' in text:
                        new_item.add_value('reg_href', link)
                    if 'информационное' in text or 'подробнее' in text:
                        new_item.add_value('source_href', response.urljoin(link))
                    if 'ссылка на официальный' in text:
                        new_item.add_value('source_href', link)

                yield new_item.load_item()


class LinguanetSpider2(scrapy.Spider):
    name = 'linguanet2'
    un_name = 'Московский государственный лингвистический университет'
    allowed_domains = ['www.linguanet.ru']
    start_urls = [
        'https://www.linguanet.ru/science/konferentsii-i-seminary/konferentsii-v-drugikh-vuzakh/'
    ]

    def parse(self, response, **kwargs):
        for line in response.xpath("//div[@class='news-index clearfix']"):
            source_href = line.css('a::attr(href)').get()
            conf_s_desc = ' '.join(i.get() for i in line.xpath('./text()'))
            if 'онференц' in conf_s_desc:
                yield scrapy.Request(
                    response.urljoin(source_href),
                    meta={'desc': conf_s_desc},
                    callback=self.parse_items,
                )

    def parse_items(self, response):
        new_item = ConferenceLoader(item=ConferenceItem(), response=response)

        new_item.add_value('source_href', response.url)
        new_item.add_xpath('title', '//h1/text()')
        new_item.add_value('short_description', response.meta.get('desc'))

        if not new_item.get_collected_values('conf_date_begin'):
            new_item = get_dates(response.meta.get('desc'), new_item)

        for line in response.xpath("//div[@class='news-detail']"):
            new_item = default_parser_xpath(line, new_item)
        yield new_item.load_item()
