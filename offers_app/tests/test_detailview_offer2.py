from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from offers_app.models import Offer, OfferDetail


class GetOffersTests(APITestCase):

    def setUp(self):
        """ Erstelle Testdaten für die API-Abfrage """
        self.user = User.objects.create_user(
            username="testuser", password="testpass")

        self.offer = Offer.objects.create(
            creator=self.user,
            title="Website Design",
            description="Professionelles Website-Design..."
        )

        self.detail1 = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Paket",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Landing Page", "Responsive Design"],
            offer_type="basic"
        )

        self.detail2 = OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Paket",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Landing Page", "Responsive Design", "Kontaktformular"],
            offer_type="standard"
        )

    def test_get_offers_success(self):
        """ Prüft, ob die API-Antwort die erwarteten Felder enthält """
        url = reverse('offer-list')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Prüfen, dass die API-Antwort die "results"-Liste enthält
        self.assertIn("results", response.data)
        # Mindestens ein Angebot
        self.assertGreater(len(response.data["results"]), 0)

        offer_data = response.data["results"][0]  # Erstes Angebot

        # Prüfen, ob alle erwarteten Felder im Offer vorhanden sind
        expected_fields = [
            "id", "user", "title", "image", "description", "created_at",
            "updated_at", "details", "min_price", "min_delivery_time"
        ]
        for field in expected_fields:
            self.assertIn(field, offer_data)

        # Prüfen, ob Details vorhanden sind
        self.assertIn("details", offer_data)
        # Mindestens ein Detail-Eintrag
        self.assertGreater(len(offer_data["details"]), 0)

        # 🛠 Basis-URL für Tests ist immer "http://testserver"
        base_url = "http://testserver"

        # ✅ Erwartete Struktur als Liste von Dictionaries
        expected_details = [
            {
                "id": self.detail1.id,
                "url": f"{base_url}{reverse('offer-detail-view', kwargs={'pk': self.detail1.id})}"
            },
            {
                "id": self.detail2.id,
                "url": f"{base_url}{reverse('offer-detail-view', kwargs={'pk': self.detail2.id})}"
            }
        ]

        # Tatsächliche Details aus der API-Antwort extrahieren
        actual_details = offer_data["details"]

        # 🔥 Vergleich der Listen von Dictionaries (Details müssen exakt übereinstimmen)
        self.assertEqual(actual_details, expected_details)

        # Prüfen, ob User-Daten korrekt enthalten sind (Optional)
        self.assertIn("user", offer_data)
        # User-ID muss passen
        self.assertEqual(offer_data["user"], self.user.id)
