from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order  # Falls du ein `Order`-Model hast


class OffersTestsSuccess(APITestCase):

    def setUp(self):
        """ Setzt Benutzer und Token für die Tests auf """
        self.offer_url = reverse('offer-list')
        self.order_url = reverse('order-list')  # Endpunkt für Order erstellen

        # Business-User erstellen
        self.user_b = User.objects.create_user(
            username="businessuser", password="password123"
        )
        self.user_b.userprofile.type = "business"
        self.user_b.userprofile.save()
        self.token_b = Token.objects.create(user=self.user_b)

        # Customer-User erstellen
        self.user_c = User.objects.create_user(
            username="customeruser", password="password123"
        )
        self.user_c.userprofile.type = "customer"
        self.user_c.userprofile.save()
        self.token_c = Token.objects.create(user=self.user_c)

        # Authentifizierungs-Header für Business-User setzen
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_b.key}')

    def test_post_offer_and_create_order(self):
        """ Testet, ob ein Business-User ein Angebot erstellt und ein Customer-User eine Bestellung dafür aufgibt """

        # 1️⃣ Business-User erstellt ein Angebot
        offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }

        response = self.client.post(self.offer_url, offer_data, format="json")

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        offer_id = response.data["id"]  # Erstellt Angebot-ID speichern
        details = response.data["details"]  # Angebotsdetails abrufen

        # 2️⃣ Authentifizierungs-Header auf Customer-User wechseln
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_c.key}')

        # 3️⃣ Customer-User gibt eine Bestellung für das "Standard Design" Angebot auf
        standard_detail = next(
            d for d in details if d["offer_type"] == "standard")

        order_data = {
            "offer": offer_id,  # Angebots-ID referenzieren
            "offer_detail": standard_detail["id"],  # Standard Design Detail
            "customer": self.user_c.id,  # Customer-User als Käufer setzen
            "status": "pending",  # Beispieldaten für den Order-Status
            "price": standard_detail["price"],  # Preis des gewählten Pakets
            "delivery_time_in_days": standard_detail["delivery_time_in_days"]
        }

        response = self.client.post(self.order_url, order_data, format="json")

        # 4️⃣ Sicherstellen, dass die Bestellung erfolgreich erstellt wurde
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 5️⃣ Sicherstellen, dass die Bestellung die richtigen Daten hat
        self.assertEqual(response.data["offer"], offer_id)
        self.assertEqual(response.data["offer_detail"], standard_detail["id"])
        self.assertEqual(response.data["customer"], self.user_c.id)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["price"], 200)
        self.assertEqual(response.data["delivery_time_in_days"], 7)
