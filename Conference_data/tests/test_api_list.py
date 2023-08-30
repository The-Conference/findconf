from django.utils import timezone

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .fixtures import TEST_CONF_DICT, TEST_CONF_FULL
from ..models import Conference, Tag


class ConferenceListTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.URL = reverse('conference-list')
        user = get_user_model()
        cls.user = user.objects.create_user(email='user@example.com', password='123')
        cls.admin = user.objects.create_superuser(email='admin@example.com', password='123')

    def setUp(self) -> None:
        self.client.raise_request_exception = False
        Conference.objects.create(**TEST_CONF_DICT)
        self.test_conf_data = TEST_CONF_DICT.copy()

    def test_list_get_200(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))
        self.assertEqual(len(response.data['results']), 1)

    def test_list_get_200_no_unchecked_in_output(self):
        self.client.post(self.URL, TEST_CONF_FULL)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_post_401(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_post_403(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.URL, self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_post_400_not_unique(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.URL, self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('conf_id')[0].code, 'unique')

    def test_list_post_400_incomplete(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data.get('un_name')[0].code, 'required')
        self.assertEqual(response.data.get('conf_date_begin')[0].code, 'required')
        self.assertEqual(response.data.get('conf_name')[0].code, 'required')
        self.assertEqual(response.data.get('conf_desc')[0].code, 'required')

    def test_list_post_201_with_conf_id(self):
        self.client.force_authenticate(user=self.admin)
        self.test_conf_data['conf_id'] = 'test02'
        response = self.client.post(self.URL, self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('conf_id'), 'test02')
        self.assertEqual(Conference.objects.all().count(), 2)

    def test_list_post_201_without_conf_id(self):
        self.client.force_authenticate(user=self.admin)
        del self.test_conf_data['conf_id']
        response = self.client.post(self.URL, self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('conf_id'), 'testunitestname2021-09-01')

    def test_list_post_all_fields_201(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.URL, TEST_CONF_FULL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in TEST_CONF_FULL.items():
            if key == 'tags':
                self.assertEqual(response.data.get('tags')[0].get('name'), 'tag01')
            else:
                self.assertEqual(response.data.get(key), value)


class ConferenceListFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.URL = reverse('conference-list')
        conf_b_data = TEST_CONF_FULL.copy()
        conf_b_data['checked'] = True
        del conf_b_data['tags']
        conf_b = Conference.objects.create(**conf_b_data)
        t1 = Tag.objects.create(name='tag_1')
        cls.t2 = t2 = Tag.objects.create(name='tag_2')
        conf_b.tags.add(t1, t2)
        cls.today = timezone.now().date()

    def setUp(self) -> None:
        self.conf: Conference = Conference.objects.create(**TEST_CONF_DICT)

    def test_list_filter_offline(self):
        response = self.client.get(f'{self.URL}?offline=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('offline'), True)

    def test_list_filter_online(self):
        response = self.client.get(f'{self.URL}?online=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('online'), True)

    def test_list_filter_rinc(self):
        response = self.client.get(f'{self.URL}?rinc=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('rinc'), True)

    def test_list_filter_vak(self):
        response = self.client.get(f'{self.URL}?vak=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('vak'), True)

    def test_list_filter_wos(self):
        response = self.client.get(f'{self.URL}?wos=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('wos'), True)

    def test_list_filter_scopus(self):
        response = self.client.get(f'{self.URL}?scopus=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('scopus'), True)

    def test_list_filter_tags(self):
        response = self.client.get(f'{self.URL}?tags=tag_1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        tag_names = [i['name'] for i in response.data['results'][0].get('tags')]
        self.assertTrue('tag_1' in tag_names)

    def test_list_filter_tags_multiple(self):
        self.conf.tags.add(self.t2)
        response = self.client.get(f'{self.URL}?tags=tag_1,tag_2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_filter_un_name(self):
        response = self.client.get(f'{self.URL}?un_name=test%20uni')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('un_name'), 'test uni')

    def test_list_filter_un_name_multiple(self):
        response = self.client.get(f'{self.URL}?un_name=test%20uni,un_name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_filter_conf_status_started(self):
        self.conf.conf_date_begin = self.today
        self.conf.conf_date_end = self.today + timezone.timedelta(days=1)
        self.conf.save()
        response = self.client.get(f'{self.URL}?conf_status=started')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('conf_status'), 'Конференция идёт')

    def test_list_filter_conf_status_starting_soon(self):
        self.conf.conf_date_begin = self.today + timezone.timedelta(days=1)
        self.conf.conf_date_end = self.today + timezone.timedelta(days=2)
        self.conf.save()
        response = self.client.get(f'{self.URL}?conf_status=starting_soon')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('conf_status'), 'Конференция скоро начнётся')

    def test_list_filter_conf_status_finished(self):
        self.conf.conf_date_begin = self.today - timezone.timedelta(days=2)
        self.conf.conf_date_end = self.today - timezone.timedelta(days=2)
        self.conf.save()
        response = self.client.get(f'{self.URL}?conf_status=finished')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0].get('conf_status'), 'Конференция окончена')

    def test_list_filter_conf_status_scheduled(self):
        self.conf.conf_date_begin = self.today + timezone.timedelta(days=20)
        self.conf.conf_date_end = self.today + timezone.timedelta(days=20)
        self.conf.save()
        response = self.client.get(f'{self.URL}?conf_status=scheduled')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('conf_status'), 'Конференция запланирована')

    def test_list_filter_conf_status_multiple(self):
        self.conf.conf_date_begin = self.today
        self.conf.conf_date_end = self.today + timezone.timedelta(days=1)
        self.conf.save()
        response = self.client.get(f'{self.URL}?conf_status=started,finished')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_filter_conf_status_nonexistent(self):
        response = self.client.get(f'{self.URL}?conf_status=nn')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_list_ordering_by_date_asc(self):
        response = self.client.get(f'{self.URL}?ordering=date_asc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['conf_date_begin'], '2021-09-01')
        self.assertEqual(response.data['results'][1]['conf_date_begin'], '2023-06-28')

    def test_list_ordering_by_date_desc(self):
        response = self.client.get(f'{self.URL}?ordering=date_desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['conf_date_begin'], '2023-06-28')
        self.assertEqual(response.data['results'][1]['conf_date_begin'], '2021-09-01')
