# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import datetime
import logging

from scrapy.exceptions import DropItem
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .models import ConferenceItemDB

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .utils import find_date_in_string


class SaveToDBPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('DATABASE_URL')
        debug = settings.get('DEBUG')
        return cls(db, debug)

    def __init__(self, db, debug):
        if debug:
            engine = create_async_engine(db, connect_args={"check_same_thread": False})
        else:
            engine = create_async_engine(db)
        self.async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def process_item(self, item, spider):
        session = self.async_session()
        async with session.begin():
            dt = ConferenceItemDB(**item)
            try:
                session.add(dt)
                await session.flush()
            except IntegrityError as e:
                await session.rollback()
                raise DropItem(e.orig)
            return item


class FillTheBlanksPipeline:
    @staticmethod
    def process_item(item, spider):
        adapter = ItemAdapter(item)
        adapter['conf_id'] = f"{spider.name}" \
                             f"_{adapter.get('conf_date_begin')}" \
                             f"_{adapter.get('conf_date_end')}" \
                             f"_{''.join(adapter.get('conf_name').split())[-30:]}"
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
            logging.warning(adapter.get('conf_card_href'))
            raise DropItem('Date not found')
        filter_date = spider.settings.get('FILTER_DATE')
        if adapter.get('conf_date_begin') < filter_date \
                or adapter.get('conf_date_end') < filter_date:
            raise DropItem(f"Old item [{adapter.get('conf_date_begin')}]")
        return item
