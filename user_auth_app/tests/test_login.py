from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="dsgdsggds"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('login')

    def test_login_success(self):
        data = {
            "username": "testuser",
            "password": "dsgdsggds"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = {"token", "username", "email", "user_id"}
        self.assertSetEqual(set(response.data.keys()), expected_keys)

        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["token"], self.token.key)

    def test_login_fail(self):
        data = {
            "username": "testuser",
            "password": "falsch"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
