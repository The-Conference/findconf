from django.utils import timezone
from django.test import TestCase

from ..models import Conference
from .fixtures import TEST_CONF_DICT


class ConferenceListTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.today = timezone.now().date()

    def test_conf_status_ongoing(self):
        current = TEST_CONF_DICT.copy()
        current['conf_date_begin'] = self.today - timezone.timedelta(days=1)
        current['conf_date_end'] = self.today + timezone.timedelta(days=1)
        conf = Conference(**current)
        self.assertEqual(conf.conf_status, 'Конференция началась')

    def test_conf_status_ended(self):
        current = TEST_CONF_DICT.copy()
        current['conf_date_begin'] = self.today - timezone.timedelta(days=5)
        current['conf_date_end'] = self.today - timezone.timedelta(days=3)
        conf = Conference(**current)
        self.assertEqual(conf.conf_status, 'Конференция окончена')

    def test_conf_status_upcoming(self):
        current = TEST_CONF_DICT.copy()
        current['conf_date_begin'] = self.today + timezone.timedelta(days=2)
        conf = Conference(**current)
        self.assertEqual(conf.conf_status, 'Конференция скоро начнётся')

    def test_conf_status_future(self):
        current = TEST_CONF_DICT.copy()
        current['conf_date_begin'] = self.today + timezone.timedelta(days=20)
        conf = Conference(**current)
        self.assertEqual(conf.conf_status, None)
