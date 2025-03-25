from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class BaseViewTests(APITestCase):

    def test_baseviews(self):
        url = reverse('base-info-list')

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = {
            "review_count",
            "average_rating",
            "business_profile_count",
            "offer_count"}
        self.assertSetEqual(set(response.data.keys()), expected_keys)
