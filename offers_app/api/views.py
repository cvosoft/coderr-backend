from rest_framework import generics, mixins
from offers_app.models import Offer
from .serializers import OfferSerializer
from rest_framework.permissions import AllowAny


# RetrieveUpdateDestroyAPIView -> für Detailansichten!
# get, put, patch, delete ist da mit drin!
class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


# für gesamtliste und fürs posten
class OffersListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
