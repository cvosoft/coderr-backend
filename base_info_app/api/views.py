from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Avg  # <--- Import für die Aggregation!
from django.contrib.auth.models import User
from reviews_app.models import Review
from offers_app.models import Offer


class BaseInfoView(APIView):
    """
    GET: Ruft allgemeine Basisinformationen zur Plattform ab.
    Keine Authentifizierung erforderlich.
    """
    permission_classes = [permissions.AllowAny]  # Offen für alle

    def get(self, request):
        # Anzahl der Bewertungen
        review_count = Review.objects.count()

        # Durchschnittliches Rating berechnen
        average_rating = Review.objects.aggregate(
            avg_rating=Avg("rating"))["avg_rating"]
        # Falls keine Bewertungen vorhanden sind
        average_rating = round(average_rating, 1) if average_rating else 0

        # Anzahl der Geschäftsnutzer (angenommen, Business-User sind in einer bestimmten Gruppe)
        business_profile_count = User.objects.filter(
            userprofile__type="business").count()

        # Anzahl der Angebote
        offer_count = Offer.objects.count()

        # Antwort zusammenstellen
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }
        return Response(data, status=status.HTTP_200_OK)
