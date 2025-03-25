from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from offers_app.models import Offer
from reviews_app.models import Reviews
from django.db.models import Avg
from profiles_app.models import UserProfile
from rest_framework import status


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Durchschnitt berechnen und auch absichern
        avg_rating = Reviews.objects.aggregate(
            average_rating=Avg('rating'))['average_rating']
        avg_rating = round(avg_rating, 1) if avg_rating is not None else 0
        review_count = Reviews.objects.count() or 0
        business_profile_count = UserProfile.objects.filter(
            type='business').count() or 0
        offer_count = Offer.objects.count() or 0

        return Response({
            "review_count": review_count,
            "average_rating": avg_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }, status=status.HTTP_200_OK)
