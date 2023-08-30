from django.utils import timezone
from django.test import TestCase

from ..models import Conference, Tag, Grant
from .fixtures import TEST_CONF_DICT


class ConferenceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.today = timezone.now().date()

    def setUp(self) -> None:
        self.test_conf_data = TEST_CONF_DICT.copy()

    def test_conf_status_ongoing(self):
        self.test_conf_data['conf_date_begin'] = self.today - timezone.timedelta(days=1)
        self.test_conf_data['conf_date_end'] = self.today + timezone.timedelta(days=1)
        conf = Conference(**self.test_conf_data)
        self.assertEqual(conf.conf_status, 'Конференция идёт')

    def test_conf_status_ended(self):
        self.test_conf_data['conf_date_begin'] = self.today - timezone.timedelta(days=5)
        self.test_conf_data['conf_date_end'] = self.today - timezone.timedelta(days=3)
        conf = Conference(**self.test_conf_data)
        self.assertEqual(conf.conf_status, 'Конференция окончена')

    def test_conf_status_upcoming(self):
        self.test_conf_data['conf_date_begin'] = self.today + timezone.timedelta(days=2)
        conf = Conference(**self.test_conf_data)
        self.assertEqual(conf.conf_status, 'Конференция скоро начнётся')

    def test_conf_status_future(self):
        self.test_conf_data['conf_date_begin'] = self.today + timezone.timedelta(days=20)
        conf = Conference(**self.test_conf_data)
        self.assertEqual(conf.conf_status, 'Конференция запланирована')

    def test_conf_status_uncertain(self):
        del self.test_conf_data['conf_date_end']
        conf = Conference(**self.test_conf_data)
        self.assertEqual(conf.conf_status, 'Дата уточняется')

    def test_conf_str(self):
        conf = Conference(**self.test_conf_data)
        self.assertEqual(str(conf), 'test uni - test name')

    def test_conf_no_id(self):
        del self.test_conf_data['conf_id']
        conf = Conference.objects.create(**self.test_conf_data)
        self.assertEqual(conf.conf_id, 'testunitestname2021-09-01')

    def test_conf_with_id(self):
        conf = Conference.objects.create(**self.test_conf_data)
        self.assertEqual(conf.conf_id, 'test01')


class TagModelTests(TestCase):
    def test_tag_str(self):
        tag = Tag(name='tag 01')
        self.assertEqual(str(tag), 'tag 01')


class GrantModelTests(TestCase):
    def test_grant_no_id(self):
        grant = Grant.objects.create(
            un_name='test uni', conf_name='test name', reg_date_end='2021-09-02')
        self.assertEqual(grant.conf_id, 'testunitestname2021-09-02')

    def test_grant_with_id(self):
        grant = Grant.objects.create(
            un_name='test uni', conf_name='test name', reg_date_end='2021-09-02', conf_id='test id')
        self.assertEqual(grant.conf_id, 'testid')
