from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .fixtures import TEST_CONF_DICT
from ..models import Conference


class ConferenceDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = get_user_model()
        cls.user = user.objects.create_user(email='user@example.com', password='123')
        cls.admin = user.objects.create_superuser(email='admin@example.com', password='123')

    def setUp(self) -> None:
        self.client.raise_request_exception = False
        self.conf = Conference.objects.create(**TEST_CONF_DICT)
        self.test_conf_data = TEST_CONF_DICT.copy()
        self.URL = reverse('conference-detail', kwargs={'pk': self.conf.pk})

    def test_detail_get_200(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get('id'), self.conf.pk)

    def test_detail_get_404(self):
        response = self.client.get(reverse('conference-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_patch_200(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.URL, data={'title': 'changed name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'changed name')

    def test_detail_put_200(self):
        self.client.force_authenticate(user=self.admin)
        self.test_conf_data['title'] = 'new name'
        response = self.client.put(self.URL, data=self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'new name')

    def test_detail_delete_204(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Conference.objects.all())

    def test_detail_delete_401(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_put_401(self):
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_patch_401(self):
        response = self.client.patch(self.URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_delete_403(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_put_403(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_patch_403(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_add_tags(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.URL, data={'tags': [{'name': 'tag_1'}]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('tags')), 1)

    def test_detail_change_tags(self):
        self.client.force_authenticate(user=self.admin)
        init_tags = [{'name': 'tag_1'}, {'name': 'tag_2'}]
        self.client.patch(self.URL, data={'tags': init_tags})
        through_table = Conference.tags.through
        self.assertEqual(through_table.objects.all().count(), 2)

        response = self.client.patch(self.URL, data={'tags': [{'name': 'tag_3'}]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('tags')), 1)

        self.assertEqual(through_table.objects.all().count(), 1)
