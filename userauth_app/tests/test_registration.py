from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class RegistrationTests(APITestCase):

    def test_registration_success(self):
        url = reverse('registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_keys = {"token", "username", "email", "user_id"}
        self.assertSetEqual(set(response.data.keys()), expected_keys)

    def test_registration_invalid_data(self):
        url = reverse('registration')
        data = {
            "username": "",
            "email": "sdffdsgds",
            "password": "pass",
            "repeated_password": "passwort123",
            "type": "dfbbfdbfd"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
