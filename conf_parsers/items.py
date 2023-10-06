# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from collections import ChainMap

from scrapy import Item, Field
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader
from urllib.parse import unquote
from pprint import pformat

from .utils import normalize_string


def absolute_url(url: str, loader_context: ChainMap) -> str:
    """Convert relative URLs to absolute.

    Args:
        url: Absolute or relative URL.
        loader_context: Parent URL, passed as a 'response' parameter of the item loader object.

    Returns:
        Absolute URL.
    """
    if loader_context.get('response') is None:
        raise ValueError(
            'No context was passed. Make sure to include response in the item loader.'
        )
    return loader_context['response'].urljoin(url)


def fix_emails(url: str) -> str:
    """Remove leftover tags."""
    return url.replace('mailto:', '')


class _AbstractItem(Item):
    """Fields common to all item types. Do not use directly."""

    item_id = Field()
    un_name = Field()
    local = Field()
    reg_date_begin = Field()
    reg_date_end = Field()
    source_href = Field()
    reg_href = Field()
    title = Field()
    short_description = Field()
    description = Field()
    contacts = Field()


class GrantItem(_AbstractItem):
    """Container for Grant items. Use in combination with ConferenceLoader."""


class ConferenceItem(_AbstractItem):
    """Container for Conference items. Use in combination with ConferenceLoader."""

    conf_date_begin = Field()
    conf_date_end = Field()
    org_name = Field()
    online = Field()
    conf_href = Field()
    offline = Field()
    conf_address = Field()
    rinc = Field()
    vak = Field()
    wos = Field()
    scopus = Field()

    def __repr__(self):
        return pformat(
            {k: v for k, v in self.items() if k != 'data'}, indent=2, compact=True, width=160
        )


class ConferenceLoader(ItemLoader):
    default_output_processor = TakeFirst()

    short_description_out = Compose(Join(), normalize_string)
    description_out = Compose(Join(), normalize_string)
    conf_address_out = Compose(Join(), normalize_string)
    contacts_out = Compose(Join(), normalize_string)

    org_name_in = MapCompose(normalize_string)
    title_in = MapCompose(normalize_string)
    source_href_in = MapCompose(unquote)
    conf_href_in = MapCompose(unquote, absolute_url, fix_emails)
    reg_href_in = MapCompose(unquote, absolute_url, fix_emails)
