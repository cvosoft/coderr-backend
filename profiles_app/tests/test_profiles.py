from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileTests(APITestCase):

    def setUp(self):
        url = reverse('registration')

        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response = self.client.post(url, data, format="json")

        self.token = response.data['token']
        self.user_id = response.data['user_id']

        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_get_profile_success(self):
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_email(self):
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id})
        data = {
            "email": "changed@gmx.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "changed@gmx.de")
