from datetime import datetime
from urllib.parse import urlencode
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import get_dates, parse_plain_text


class KpfuSpider(scrapy.Spider):
    name = "kpfu"
    un_name = 'Казанский (Приволжский) федеральный университет'
    allowed_domains = ["kpfu.ru"]

    def start_requests(self):
        url = "https://kpfu.ru/portal_new.main_page?"
        year = datetime.now().year
        querystring = {"p_sub": "49618", "p_group_name": "", "p_meropriatie_vid_type": "2", "p_kon_kfu": "1",
                       "p_mounth_date": "", "p_year_start": year, "status": "", "p_office": "", "p_date_start": "",
                       "p_date_end": "", "p_page": "1"}
        yield scrapy.Request(url=url + urlencode(querystring), callback=self.parse_page)

    def parse_page(self, response):
        for row in response.xpath("//table//tr[@class='konf_tr']"):
            new_item = ConferenceLoader(item=ConferenceItem(), selector=row)
            conf_name = row.css('td:nth-child(2) ::text').get()
            new_item.add_value('conf_name', conf_name)
            new_item.add_value('conf_card_href', response.url)
            dates = row.css('td:nth-child(3)::text').get()
            new_item = get_dates(dates, new_item)
            new_item = parse_plain_text(conf_name, new_item)
            new_item.add_xpath('conf_address', "string(./td[position()=4])")
            yield new_item.load_item()

        if next_link := response.xpath("//div[@class='pagination']/a[contains(text(), '»')]/@href").get():
            yield scrapy.Request(next_link, callback=self.parse_page)
