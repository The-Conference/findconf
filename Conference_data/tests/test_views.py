from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .fixtures import TEST_CONF_DICT, TEST_CONF_FULL
from ..models import Conference


class ConferenceListTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.URL = reverse('conf-list')
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
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 1)

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
        self.assertEqual(response.data.get('conf_id')[0].code, 'required')
        self.assertEqual(response.data.get('un_name')[0].code, 'required')
        self.assertEqual(response.data.get('conf_date_begin')[0].code, 'required')
        self.assertEqual(response.data.get('conf_name')[0].code, 'required')

    def test_list_post_201(self):
        self.client.force_authenticate(user=self.admin)
        self.test_conf_data['conf_id'] = 'test02'
        response = self.client.post(self.URL, self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Conference.objects.all()), 2)

    def test_list_post_all_fields_201(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.URL, TEST_CONF_FULL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in TEST_CONF_FULL.items():
            self.assertEqual(response.data.get(key), value)


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
        self.URL = reverse('conf-detail', kwargs={'pk': self.conf.pk})

    def test_detail_get_200(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get('id'), self.conf.pk)

    def test_detail_get_404(self):
        response = self.client.get(reverse('conf-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_patch_200(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.URL, data={'conf_name': 'changed name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('conf_name'), 'changed name')

    def test_detail_put_200(self):
        self.client.force_authenticate(user=self.admin)
        self.test_conf_data['conf_name'] = 'new name'
        response = self.client.put(self.URL, data=self.test_conf_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('conf_name'), 'new name')

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
