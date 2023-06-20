import re
import scrapy

from ..items import ConferenceItem, ConferenceLoader
from ..parsing import default_parser_xpath, get_dates


class StankinSpider(scrapy.Spider):
    name = "stankin"
    un_name = 'Московский государственный технологический университет «СТАНКИН»'
    allowed_domains = ["stankin.ru"]
    api_url = "https://stankin.ru/api_entry.php"
    base_url = "https://stankin.ru/pages/id_82/page_"

    def start_requests(self):
        payload = {
            "action": "getTemplateCategory",
            "data": {"id": "82"}
        }
        yield scrapy.http.JsonRequest(self.api_url, data=payload, callback=self.parse_links)

    def parse_links(self, response):
        for item in response.json().get("data").get("menu"):
            name = item.get("name")
            modals = item.get("modals")
            pages = item.get("pages")
            _id = 0
            if modals:
                _id = modals[0].get("id")
            if pages:
                _id = pages[0].get("id")
            payload = {
                "action": "getTemplateCategoryPage",
                "data": {"id": _id}
            }
            yield scrapy.http.JsonRequest(self.api_url, data=payload, callback=self.parse_items,
                                          meta={"name": name, "id": str(_id)})

    def parse_items(self, response):
        data = response.json().get("data").get("delta").get("delta").get("ops")
        text = [i.get("insert") for i in data if not isinstance(i.get("insert"), dict)]
        text = " ".join(text)
        if 'конфер' in text.lower():
            new_item = ConferenceLoader(item=ConferenceItem(), selector=response)
            new_item.add_value('conf_card_href', self.base_url + response.meta.get("id"))
            new_item.add_value('conf_name', response.meta.get("name"))

            for line in re.split(r"\s+\n", text):
                new_item = default_parser_xpath(line, new_item)
            if not new_item.get_collected_values('conf_date_begin'):
                new_item = get_dates(new_item.get_output_value('conf_desc'), new_item)
            yield new_item.load_item()
