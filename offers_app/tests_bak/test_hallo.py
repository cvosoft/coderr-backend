from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from offers_app.models import Offer, OfferDetail


class OfferDetailViewTest(APITestCase):

    def setUp(self):
        """ Erstellt einen Benutzer, ein Angebot und Details für den Test """
        self.user = User.objects.create_user(
            username="testuser", password="dsgdsggds"
        )

        self.user.userprofile.type = "business"
        self.user.userprofile.save()

        # Authentifizierungstoken erstellen
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Angebot erstellen
        self.offer = Offer.objects.create(
            creator=self.user,
            title="Grafikdesign-Paket",
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen."
        )

        # Angebotsdetails erstellen
        self.detail1 = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )

        self.detail2 = OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard"
        )

        self.detail3 = OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium"
        )

    def test_offer_detail_view(self):
        """ Testet, ob die Detailansicht eines Angebots korrekt ausgegeben wird """
        url = reverse('offer-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url, format="json")

        # Prüfe Status-Code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Prüfe ob alle erwarteten Felder enthalten sind
        expected_fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", "details", "min_price", "min_delivery_time"
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

        # Prüfe den Wert des Angebots
        self.assertEqual(response.data["id"], self.offer.id)
        self.assertEqual(response.data["title"], self.offer.title)
        self.assertEqual(response.data["description"], self.offer.description)

        # Prüfe, dass die min_price und min_delivery_time korrekt berechnet wurden
        # Günstigste Preisstufe
        self.assertEqual(response.data["min_price"], 100)
        # Kürzeste Lieferzeit
        self.assertEqual(response.data["min_delivery_time"], 5)

        # Prüfe, ob alle Details enthalten sind
        self.assertEqual(len(response.data["details"]), 3)

        # 🛠 Basis-URL für Tests ist immer "http://testserver"
        base_url = "http://testserver"

        expected_detail_urls = [
            {
                "id": self.detail1.id,
                "url": f"{base_url}{reverse('offer-detail-view', kwargs={'pk': self.detail1.id})}"
            },
            {
                "id": self.detail2.id,
                "url": f"{base_url}{reverse('offer-detail-view', kwargs={'pk': self.detail2.id})}"
            },
            {
                "id": self.detail3.id,
                "url": f"{base_url}{reverse('offer-detail-view', kwargs={'pk': self.detail3.id})}"
            },
        ]

        # Tatsächliche Detail-URLs aus der API-Antwort extrahieren
        actual_detail_urls = response.data["details"]

        # 🔥 Vergleich der Listen von Dictionaries (Details müssen exakt übereinstimmen)
        self.assertEqual(actual_detail_urls, expected_detail_urls)
