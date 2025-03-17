from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from reviews_app.models import Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class GetOffersTests(APITestCase):

    def test_get_offers_success(self):
        url = reverse('offer-list')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
