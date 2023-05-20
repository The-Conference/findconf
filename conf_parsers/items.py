# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader
from .utils import normalise_str


class ConferenceItem(scrapy.Item):
    conf_id = scrapy.Field()
    hash = scrapy.Field()
    un_name = scrapy.Field()
    local = scrapy.Field()
    reg_date_begin = scrapy.Field()
    reg_date_end = scrapy.Field()
    conf_date_begin = scrapy.Field()
    conf_date_end = scrapy.Field()
    conf_card_href = scrapy.Field()
    reg_href = scrapy.Field()
    conf_name = scrapy.Field()
    conf_s_desc = scrapy.Field()
    conf_desc = scrapy.Field()
    org_name = scrapy.Field()
    themes = scrapy.Field()
    online = scrapy.Field()
    conf_href = scrapy.Field()
    offline = scrapy.Field()
    conf_address = scrapy.Field()
    contacts = scrapy.Field()
    rinc = scrapy.Field()
    data = scrapy.Field()
    checked = scrapy.Field()
    vak = scrapy.Field()
    wos = scrapy.Field()
    scopus = scrapy.Field()


class ConferenceLoader(ItemLoader):
    default_output_processor = TakeFirst()

    conf_s_desc_in = MapCompose(normalise_str)
    conf_s_desc_out = Join(' ')
    conf_desc_in = MapCompose(normalise_str)
    conf_desc_out = Join(' ')
    org_name_in = MapCompose(normalise_str)
    conf_address_in = MapCompose(normalise_str)
    conf_address_out = Join(' ')
    contacts_in = MapCompose(normalise_str)
    contacts_out = Join(' ')
    conf_name_in = MapCompose(normalise_str)
