from unittest import TestCase

from conf_parsers.models import ConferenceItemDB


class TestModels(TestCase):
    def test_string_too_long(self):
        long_string = 'X' * 600
        db_item = ConferenceItemDB(conf_card_href=long_string)
        self.assertEqual(500, len(db_item.conf_card_href))

    def test_string_ok(self):
        long_string = 'X' * 100
        db_item = ConferenceItemDB(conf_card_href=long_string)
        self.assertEqual(100, len(db_item.conf_card_href))
