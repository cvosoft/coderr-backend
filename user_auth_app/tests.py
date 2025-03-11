from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.


class RegistrationTests(APITestCase):

    def test_registration(self):
        url = reverse('registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
