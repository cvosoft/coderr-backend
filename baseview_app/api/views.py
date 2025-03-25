from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from offers_app.models import Offer
from reviews_app.models import Reviews
from django.db.models import Avg
from profiles_app.models import UserProfile


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "review_count": Reviews.objects.count(),
            "average_rating": Reviews.objects.aggregate(average_rating=Avg('rating'))['average_rating'],
            "business_profile_count": UserProfile.objects.filter(type='business').count(),
            "offer_count": Offer.objects.count()
        })
