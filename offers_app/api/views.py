from rest_framework import generics
from offers_app.models import Offer
from .serializers import OfferSerializer


class OffersViewList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
