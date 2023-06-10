import datetime
from unittest import TestCase

from scrapy.http import HtmlResponse, Request
from scrapy.utils.project import get_project_settings

from conf_parsers.items import ConferenceLoader, ConferenceItem
from conf_parsers.parsing import default_parser_xpath, parse_plain_text, get_dates


class TestParsing(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = get_project_settings().get('ROOT_DIR')
        sample = root.joinpath('conf_parsers', 'tests', 'test_conf.htm')
        url = 'http://www.example.com'
        request = Request(url=url)
        with open(sample, 'rb') as f:
            response = HtmlResponse(url=url, request=request, body=f.read(), encoding='utf-8')
        loader = ConferenceLoader(item=ConferenceItem(), selector=response)
        for line in response.xpath("//div[@class='news-item']//*[self::p]"):
            loader = default_parser_xpath(line, loader)
        cls.new_item = loader
        cls.response = response

    def test_sample_registration(self):
        self.assertEqual('http://example.com/321/', self.new_item.get_output_value('reg_href'))
        self.assertEqual([datetime.date(2020, 5, 20), datetime.date(2020, 4, 11)],
                         self.new_item.get_collected_values('reg_date_end'))
        self.assertEqual(datetime.date(2020, 5, 20), self.new_item.get_output_value('reg_date_end'))
        self.assertEqual(datetime.date(2020, 5, 15), self.new_item.get_output_value('reg_date_begin'))

    def test_sample_dates(self):
        self.assertEqual(datetime.date(2021, 6, 11), self.new_item.get_output_value('conf_date_end'))
        self.assertEqual(datetime.date(2021, 6, 10), self.new_item.get_output_value('conf_date_begin'))

    def test_sample_contacts(self):
        self.assertEqual(['Контактное лицо: Иванов Иван Иванович', 'plaintext@example.com'],
                         self.new_item.get_collected_values('contacts'))

    def test_sample_bools(self):
        self.assertTrue(self.new_item.get_output_value('online'))
        self.assertTrue(self.new_item.get_output_value('offline'))
        self.assertTrue(self.new_item.get_output_value('wos'))
        self.assertTrue(self.new_item.get_output_value('vak'))
        self.assertTrue(self.new_item.get_output_value('scopus'))
        self.assertTrue(self.new_item.get_output_value('rinc'))

    def test_sample_address(self):
        self.assertEqual('Место проведения: г.Н-ск, ул. Тестовая', self.new_item.get_output_value('conf_address'))

    def test_sample_conf(self):
        self.assertEqual(10, len(self.new_item.get_collected_values('conf_desc')))
        self.assertEqual('http://example.com/123/', self.new_item.get_output_value('conf_href'))

    def test_text_parser_sample_contacts(self):
        new_item = ConferenceLoader(item=ConferenceItem(), selector=self.response)
        for line in self.response.xpath("//div[@class='news-item']//*[self::p]"):
            line = line.xpath("string(.)").get()
            new_item = parse_plain_text(line, new_item)
        self.assertEqual(['Контактное лицо: Иванов Иван Иванович', 'plaintext@example.com'],
                         self.new_item.get_collected_values('contacts'))


class TestGetDates(TestCase):
    def setUp(self) -> None:
        self.new_item = ConferenceLoader(item=ConferenceItem())

    def test_get_dates_regular_single(self):
        line = '11 апреля 2020'
        result = get_dates(line, self.new_item)
        self.assertEqual([datetime.date(2020, 4, 11)], result.get_collected_values('conf_date_begin'))
        self.assertFalse(result.get_output_value('conf_date_end'))

    def test_get_dates_regular_double(self):
        line = '11-12 апреля 2020'
        result = get_dates(line, self.new_item)
        self.assertEqual([datetime.date(2020, 4, 11)], result.get_collected_values('conf_date_begin'))
        self.assertEqual([datetime.date(2020, 4, 12)], result.get_collected_values('conf_date_end'))

    def test_get_dates_vague(self):
        line = 'апрель 2020'
        result = get_dates(line, self.new_item, is_vague=True)
        self.assertEqual([datetime.date(2020, 4, 1)], result.get_collected_values('conf_date_begin'))
        self.assertEqual([datetime.date(2020, 4, 30)], result.get_collected_values('conf_date_end'))
