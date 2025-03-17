from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from reviews_app.models import Review  # Import für Mocking


class BaseViewTests(APITestCase):

    def test_baseview_success(self):
        url = reverse('base-info')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = {"review_count", "average_rating",
                         "business_profile_count", "offer_count"}
        self.assertSetEqual(set(response.data.keys()), expected_keys)

    @patch("reviews_app.models.Review.objects.count", side_effect=Exception("Datenbankfehler!"))
    def test_baseview_internal_server_error(self, mock_count):
        url = reverse('base-info')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Ein interner Serverfehler ist aufgetreten.")
