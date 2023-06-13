from unittest import TestCase

from scrapy import Request
from scrapy.http import HtmlResponse

from conf_parsers.models import ConferenceItemDB
from conf_parsers.items import ConferenceLoader, ConferenceItem


class TestModels(TestCase):
    def test_string_too_long(self):
        long_string = 'X' * 600
        db_item = ConferenceItemDB(conf_card_href=long_string)
        self.assertEqual(500, len(db_item.conf_card_href))

    def test_string_ok(self):
        long_string = 'X' * 100
        db_item = ConferenceItemDB(conf_card_href=long_string)
        self.assertEqual(100, len(db_item.conf_card_href))


class TestItemLoader(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        url = 'http://example.com'
        cls.response = HtmlResponse(url=url, request=Request(url=url))
        cls.href_fields = ('reg_href', 'conf_href')
        cls.text_fields = ('conf_s_desc', 'conf_desc', 'conf_address', 'contacts')

    def setUp(self) -> None:
        self.loader = ConferenceLoader(item=ConferenceItem(), selector=self.response)

    def test_clean_email(self):
        string = 'mailto:test@example.com'
        for field in self.href_fields:
            self.loader.add_value(field, string)
            self.assertEqual('test@example.com', self.loader.get_output_value(field))

    def test_relative_to_absolute_url(self):
        string = '/111/222/'
        expected = 'http://example.com/111/222/'
        for field in self.href_fields:
            self.loader.add_value(field, string)
            self.assertEqual(expected, self.loader.get_output_value(field))

    def test_absolute_url(self):
        string = 'http://example.net/111/222/'
        for field in self.href_fields:
            self.loader.add_value(field, string)
            self.assertEqual(string, self.loader.get_output_value(field))

    def test_unquote_encoded_url(self):
        string = 'http%3A%2F%2Fexample.com%2F%D1%82%D0%B5%D1%81%D1%82%2F'
        expected = 'http://example.com/тест/'
        for field in 'conf_card_href', *self.href_fields:
            self.loader.add_value(field, string)
            self.assertEqual(expected, self.loader.get_output_value(field))

    def test_clean_url_all(self):
        string1 = '%2F%D1%82%D0%B5%D1%81%D1%82%2F'
        string2 = 'mailto:test@example.com'
        expected = ['http://example.com/тест/', 'test@example.com']
        for field in self.href_fields:
            self.loader.add_value(field, string1)
            self.loader.add_value(field, string2)
            self.assertEqual(expected, self.loader.get_collected_values(field))

    def test_string_processing(self):
        string1 = '\r\r\r\n\ntest\r\r\r\n\n'
        string2 = 'another&nbsp;line'
        for field in self.text_fields:
            self.loader.add_value(field, string1)
            self.loader.add_value(field, string2)
            expected = 'test another line'
            self.assertEqual(expected, self.loader.get_output_value(field))
