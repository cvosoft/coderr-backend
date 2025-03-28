from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# Create your tests here.


class PatchOrdersTests(APITestCase):

    def setUp(self):
        url = reverse('registration')

        data_busi = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business"
        }

        data_cust = {
            "username": "exampleUsername2",
            "email": "example2@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        response1 = self.client.post(url, data_busi, format="json")
        response2 = self.client.post(url, data_cust, format="json")

        # variablen in self speichern, dann sind sie global verfügbar
        self.token1 = response1.data['token']
        self.user_id1 = response1.data['user_id']
        self.token2 = response2.data['token']
        self.user_id2 = response2.data['user_id']

        # Authentifizierungs-Header setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')

        # offer erstellen
        url = reverse('offers-list')
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(url, data, format="json")
        self.offerdetail_id = response.data['details'][0]['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        url = reverse('orders-list')
        data = {
            "offer_detail_id": self.offerdetail_id
        }
        response = self.client.post(url, data, format="json")
        self.order_id = response.data['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_keys = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_patch_order_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        data = {
            "status": "completed"
        }

        url = reverse('orders-detail', kwargs={'pk': self.order_id})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]

        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_patch_order_no_auth(self):
        self.client.credentials()
        data = {
            "status": "completed"
        }

        url = reverse('orders-detail', kwargs={'pk': self.order_id})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_as_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        data = {
            "status": "completed"
        }

        url = reverse('orders-detail', kwargs={'pk': self.order_id})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_as_staff(self):
        # neuen staff user
        url = reverse('registration')

        data_staff = {
            "username": "staffi",
            "email": "staffi@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business"
        }
        response = self.client.post(url, data_staff, format="json")
        self.token = response.data['token']
        self.user_id = response.data['user_id']
        user = User.objects.get(id=self.user_id)
        user.is_staff = True
        user.save()
        # einloggen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        url = reverse('orders-detail', kwargs={'pk': self.order_id})

        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_order_count_no_auth(self):
        self.client.credentials()
        url = reverse('order-count', kwargs={'business_user': self.user_id1})

        response = self.client.get(url, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_count_auth(self):

        url = reverse('order-count', kwargs={'business_user': self.user_id1})

        response = self.client.get(url, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_no_business(self):

        url = reverse('order-count', kwargs={'business_user': self.user_id2})

        response = self.client.get(url, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_count_auth(self):

        url = reverse('completed-order-count',
                      kwargs={'business_user': self.user_id1})

        response = self.client.get(url, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 0)
        # complete setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        data = {
            "status": "completed"
        }

        url = reverse('orders-detail', kwargs={'pk': self.order_id})

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # neu zählen
        url = reverse('completed-order-count',
                      kwargs={'business_user': self.user_id1})

        response = self.client.get(url, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)
