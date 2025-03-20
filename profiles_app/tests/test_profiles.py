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
            "type": "business"
        }

        response = self.client.post(url, data, format="json")

        # variablen in self speichern, dann sind sie global verfügbar
        self.token = response.data['token']
        self.user_id = response.data['user_id']

        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # weiterer user
        data2 = {
            "username": "exampleUsername2",
            "email": "example2@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business"
        }
        response = self.client.post(url, data2, format="json")
        #print(response.data)
        self.user_id2 = response.data['user_id']

    def test_get_profile_success(self):
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_no_auth(self):
        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token xxx')
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_email(self):
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id})
        data = {
            "email": "changed@gmx.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "changed@gmx.de")

    def test_patch_profile_email_wrong_user(self):
        url = reverse('profile-detail',
                      kwargs={'user': self.user_id2})
        data = {
            "email": "changed@gmx.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
