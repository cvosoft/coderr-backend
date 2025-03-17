from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BaseViewTests(APITestCase):

    def test_baseview(self):

        url = reverse('base-info')

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = {"review_count", "average_rating",
                         "business_profile_count", "offer_count", }
        self.assertSetEqual(set(response.data.keys()), expected_keys)
