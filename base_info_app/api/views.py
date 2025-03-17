from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Avg
from django.contrib.auth.models import User
from reviews_app.models import Review
from offers_app.models import Offer


class BaseInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            #reviews zaehlen
            review_count = Review.objects.count()

            #durchschnitt der ratings berechnen
            average_rating = Review.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"]
            average_rating = round(average_rating, 1) if average_rating else 0

            #business profile zaehlen
            business_profile_count = User.objects.filter(userprofile__type="business").count()

            #offers zaehlen
            offer_count = Offer.objects.count()

            data = {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Ein interner Serverfehler ist aufgetreten."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
