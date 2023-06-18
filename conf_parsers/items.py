# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader
from urllib.parse import unquote
from pprint import pformat

from .utils import normalize_string


def absolute_url(url, loader_context):
    """Convert relative URLs to absolute."""
    return loader_context['selector'].urljoin(url)


def fix_emails(url):
    """Remove leftover tags."""
    return url.replace('mailto:', '')


class ConferenceItem(Item):
    conf_id = Field()
    hash = Field()
    un_name = Field()
    local = Field()
    reg_date_begin = Field()
    reg_date_end = Field()
    conf_date_begin = Field()
    conf_date_end = Field()
    conf_card_href = Field()
    reg_href = Field()
    conf_name = Field()
    conf_s_desc = Field()
    conf_desc = Field()
    org_name = Field()
    themes = Field()
    online = Field()
    conf_href = Field()
    offline = Field()
    conf_address = Field()
    contacts = Field()
    rinc = Field()
    data = Field()
    checked = Field()
    vak = Field()
    wos = Field()
    scopus = Field()

    def __repr__(self):
        return pformat({k: v for k, v in self.items() if k != 'data'},
                       indent=2, compact=True, width=160)


class ConferenceLoader(ItemLoader):
    default_output_processor = TakeFirst()

    conf_s_desc_out = Compose(Join(), normalize_string)
    conf_desc_out = Compose(Join(), normalize_string)
    conf_address_out = Compose(Join(), normalize_string)
    contacts_out = Compose(Join(), normalize_string)

    org_name_in = MapCompose(normalize_string)
    conf_name_in = MapCompose(normalize_string)
    conf_card_href_in = MapCompose(unquote)
    conf_href_in = MapCompose(unquote, absolute_url, fix_emails)
    reg_href_in = MapCompose(unquote, absolute_url, fix_emails)
