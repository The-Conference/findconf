# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib
import datetime

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import ConferenceItemDB
from .utils import find_date_in_string


class SaveToDBPipeline:
    """Use bulk insert to save items to PostgreSQL.
    Items with duplicate conf_id are ignored.
    Does not raise DropItem exceptions."""
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('DATABASE_URL')
        return cls(db)

    def __init__(self, db):
        self.engine = create_engine(db)
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        insert_statement = insert(ConferenceItemDB).values(self.items).returning(ConferenceItemDB.conf_id)
        insert_or_do_nothing = insert_statement.on_conflict_do_nothing(index_elements=[ConferenceItemDB.conf_id])
        to_save = [i.get("conf_id") for i in self.items]
        spider.logger.debug(f'Saving to DB: {to_save}')

        if to_save:
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
    @staticmethod
    def process_item(item, spider):
        adapter = ItemAdapter(item)
        adapter['conf_id'] = f"{spider.name}" \
                             f"_{adapter.get('conf_date_begin')}" \
                             f"_{adapter.get('conf_date_end')}" \
                             f"_{''.join(adapter.get('conf_name').split())[:50]}"
        adapter['un_name'] = spider.un_name
        adapter['hash'] = hashlib.md5(bytes(adapter['conf_id'], 'utf-8')).hexdigest()
        adapter['data'] = {key: val.strftime("%m/%d/%Y") if isinstance(val, datetime.date) else val
                           for key, val in item.items()}
        text = f"{adapter.get('conf_name')} {adapter.get('conf_s_desc')}"
        adapter['local'] = False if 'международн' in text.lower() else True
        return item


class DropOldItemsPipeline:
    @staticmethod
    def process_item(item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('conf_date_begin'):
            # look for dates in the short description
            if dates := find_date_in_string(adapter.get('conf_s_desc')):
                adapter['conf_date_begin'] = dates[0]
                adapter['conf_date_end'] = dates[1] if len(dates) > 1 else dates[0]

        if not adapter.get('conf_date_begin'):
            spider.logger.warning(f"Date not found {adapter.get('conf_card_href')}")
            spider.logger.debug(item)
            raise DropItem('Date not found')
        filter_date = spider.settings.get('FILTER_DATE')
        if adapter.get('conf_date_begin') < filter_date:
            raise DropItem(f"Old item [{adapter.get('conf_date_begin')}]")
        return item
