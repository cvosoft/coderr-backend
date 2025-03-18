from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from reviews_app.models import Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileTests(APITestCase):

    def setUp(self):
        self.url = reverse('offer-list')
        self.user = User.objects.create_user(
            username="testuser", password="dsgdsggds"
        )

        self.user.userprofile.type = "customer"
        self.user.userprofile.save()

        # Token für den Benutzer erstellen
        self.token = Token.objects.create(user=self.user)

        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_profile_success(self):
        url = reverse('userprofile-detail',
                      kwargs={'user': self.user.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_email(self):
        url = reverse('userprofile-detail',
                      kwargs={'user': self.user.id})
        data = {
            "email": "changed@gmx.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "changed@gmx.de")
