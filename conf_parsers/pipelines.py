"""Pipelines are called automatically by Scrapy. No direct usage."""

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import ConferenceItemDB, GrantItemDB
from .utils import find_date_in_string
from .items import ConferenceItem, GrantItem


class SaveToDBPipeline:
    """Use bulk insert to save items to PostgreSQL.
    Items with duplicate item_id are ignored.
    Does not raise DropItem exceptions."""
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('DATABASE_URL')
        return cls(db)

    def __init__(self, db):
        self.engine = create_engine(db)
        self.items = []
        self.item_type = None

    def process_item(self, item, spider):
        if isinstance(item, ConferenceItem):
            self.item_type = ConferenceItemDB
        elif isinstance(item, GrantItem):
            self.item_type = GrantItemDB
        else:
            raise TypeError('Unknown item type. Add appropriate model to SaveToDBPipeline.')
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        to_save = [i.get("item_id") for i in self.items]
        spider.logger.debug(f'Saving to DB: {to_save}')

        if to_save:
            insert_statement = insert(self.item_type).values(self.items).returning(self.item_type.item_id)
            insert_or_do_nothing = insert_statement.on_conflict_do_nothing(index_elements=[self.item_type.item_id])
            try:
                saved = self.session.execute(insert_or_do_nothing).fetchall()
                self.session.commit()
                saved = [i[0] for i in saved]
                spider.logger.info(f'Saved {len(saved)} items to DB: {saved}')
                spider.logger.info(f'Duplicate items: {set(to_save).symmetric_difference(saved)}')
            except IntegrityError:
                self.session.rollback()
                raise
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)


class FillTheBlanksPipeline:
    """Fill out fields that are derived from other fields."""
    @staticmethod
    def process_item(item, spider):
        adapter = ItemAdapter(item)

        adapter['un_name'] = spider.un_name
        text = f"{adapter.get('title')} {adapter.get('short_description')}"
        adapter['local'] = False if 'международн' in text.lower() else True

        if isinstance(item, ConferenceItem):
            adapter['item_id'] = f"{spider.name}" \
                                 f"_{adapter.get('conf_date_begin')}" \
                                 f"_{adapter.get('conf_date_end')}" \
                                 f"_{''.join(adapter.get('title').split())[:50]}"
            if not adapter.get('conf_date_end'):
                adapter['conf_date_end'] = adapter.get('conf_date_begin')

        elif isinstance(item, GrantItem):
            adapter['item_id'] = f"{spider.name}" \
                                 f"_{adapter.get('reg_date_end')}" \
                                 f"_{''.join(adapter.get('title').split())[:50]}"
        return item


class DropOldItemsPipeline:
    """Check parsed item against FILTER_DATE parameter;
    attempt to fill the date if none is parsed;
    drop item if check fails.

    Raises:
        DropItem: if the date is not found or too old."""
    @staticmethod
    def process_item(item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, ConferenceItem):
            lookup_date_field = 'conf_date_begin'
            if not adapter.get(lookup_date_field) and adapter.get('short_description'):
                # look for dates in the short description
                if dates := find_date_in_string(adapter.get('short_description')):
                    adapter[lookup_date_field] = dates[0]
                    adapter['conf_date_end'] = dates[1] if len(dates) > 1 else None
        elif isinstance(item, GrantItem):
            lookup_date_field = 'reg_date_end'
        else:
            raise ValueError('Unknown main date for this item.')

        date = adapter.get(lookup_date_field)
        if not date:
            spider.logger.warning(f"Date not found {adapter.get('source_href')}")
            spider.logger.debug(item)
            raise DropItem('Date not found')
        filter_date = spider.settings.get('FILTER_DATE')
        if date < filter_date:
            raise DropItem(f"Old item [{date}]")
        return item
