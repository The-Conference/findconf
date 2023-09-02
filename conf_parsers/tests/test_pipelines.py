import datetime
from unittest import TestCase
from datetime import date, datetime

import scrapy
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from conf_parsers.items import ConferenceItem
from conf_parsers.pipelines import DropOldItemsPipeline, SaveToDBPipeline, FillTheBlanksPipeline
from conf_parsers.models import Base, ConferenceItemDB


class SampleSpider(scrapy.Spider):
    name = 'test_spider'
    un_name = 'Test Spider 2000'
    settings = get_project_settings()
    settings['DATABASE_URL'] = "sqlite:///file:test_db?cache=shared&mode=memory&uri=true"


class TestDropOldItemsPipeline(TestCase):
    def setUp(self) -> None:
        self.spider = SampleSpider()

    def test_old(self):
        item = ConferenceItem(conf_date_begin=date(1970, 1, 1))
        with self.assertRaises(DropItem) as e:
            DropOldItemsPipeline.process_item(item, self.spider)
        self.assertEqual('Old item [1970-01-01]', str(e.exception))

    def test_new(self):
        item = ConferenceItem(conf_date_begin=datetime.now().date())
        self.assertTrue(DropOldItemsPipeline.process_item(item, self.spider))

    def test_no_date(self):
        item = ConferenceItem()
        with self.assertRaises(DropItem) as e:
            DropOldItemsPipeline.process_item(item, self.spider)
        self.assertEqual('Date not found', str(e.exception))

    def test_date_found_new(self):
        today = datetime.now().date()
        str_today = f'{today.day}-{today.month}-{today.year}'
        item = ConferenceItem(short_description=str_today)
        expected = {'conf_date_begin': today, 'conf_date_end': None, 'short_description': str_today}
        self.assertEqual(expected, DropOldItemsPipeline.process_item(item, self.spider))

    def test_date_not_found(self):
        item = ConferenceItem(short_description='test')
        with self.assertRaises(DropItem) as e:
            DropOldItemsPipeline.process_item(item, self.spider)
        self.assertEqual('Date not found', str(e.exception))


class TestSaveToDBPipeline(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.item = ConferenceItem(
            item_id='test',
            un_name='test_spider',
            conf_date_begin=datetime.now().date(),
            description='',
            title='test conf',
        )
        cls.db_item = ConferenceItemDB(**cls.item)
        cls.spider = SampleSpider()
        cls.db_url = 'sqlite:///file:test_db?cache=shared&mode=memory&uri=true'
        engine = create_engine(cls.db_url)
        cls.session = Session(bind=engine)
        Base.metadata.create_all(engine)

    def setUp(self) -> None:
        self.db = SaveToDBPipeline(self.db_url)
        self.db.open_spider(self.spider)

    def tearDown(self) -> None:
        self.session.query(ConferenceItemDB).delete()
        self.session.commit()

    def test_save_to_db(self):
        self.db.process_item(self.item, self.spider)
        self.db.close_spider(self.spider)

        q = select(ConferenceItemDB).where(ConferenceItemDB.id == 1)
        res = self.session.execute(q).scalars().first()
        self.assertTrue(res)
        self.assertEqual('test', res.item_id)

    def test_save_duplicate_id(self):
        self.session.add(self.db_item)
        self.session.commit()
        self.db.process_item(self.item, self.spider)

        with self.assertLogs(level='INFO') as log:
            self.db.close_spider(self.spider)
            self.assertEqual(['INFO:test_spider:Saved 0 items to DB: []',
                              "INFO:test_spider:Duplicate items: {'test'}"], log.output)
        q = select(ConferenceItemDB)
        res = self.session.execute(q).scalars().all()
        self.assertEqual(1, len(res))

    def test_save_incomplete_data(self):
        item = ConferenceItem()
        self.db.process_item(item, self.spider)
        with self.assertRaises(IntegrityError):
            self.db.close_spider(self.spider)

    def test_save_nothing(self):
        with self.assertLogs(level='DEBUG') as log:
            self.db.close_spider(self.spider)
        self.assertEqual(['DEBUG:test_spider:Saving to DB: []'], log.output)

    def test_setup(self):
        pipeline_class = SaveToDBPipeline.from_crawler(self.spider)
        self.assertEqual(SampleSpider.settings.get('DATABASE_URL'), str(pipeline_class.engine.url))


class TestFillTheBlanksPipeline(TestCase):
    def test_item_id_single(self):
        """Do not change.
        Changing item_id format will result in duplicate entries in DB."""
        item = ConferenceItem(
            conf_date_begin=date(2022, 1, 2),
            title='test conf',
        )
        result = FillTheBlanksPipeline.process_item(item, SampleSpider)
        self.assertEqual('test_spider_2022-01-02_None_testconf', result['item_id'])

    def test_item_id_double(self):
        """Do not change.
        Changing item_id format will result in duplicate entries in DB."""
        item = ConferenceItem(
            conf_date_begin=date(2022, 1, 2),
            conf_date_end=date(2022, 1, 3),
            title='test conf',
        )
        result = FillTheBlanksPipeline.process_item(item, SampleSpider)
        self.assertEqual('test_spider_2022-01-02_2022-01-03_testconf', result['item_id'])
