from rest_framework import generics, mixins
from offers_app.models import Offer, OfferDetails
from .serializers import SingleOfferListSerializer, OfferWriteSerializer, OffersListSerializer, OfferDetailSerializer, OfferDetailURLSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import ResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter
from .permissions import IsBusinessUser, IsOwnerOrAdmin
from rest_framework import viewsets


################
# GET /api/offers/ - list
# POST /api/offers/ - create
# GET /api/offers/{id}/ - retrieve
# PATCH /api/offers/{id}/ - partial update
# DELETE /api/offers/{id}/ - destroy
#################

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    pagination_class = ResultsSetPagination

    # Einteilung Serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return OffersListSerializer  # Für /api/offers/
        elif self.action == 'create':
            return OfferWriteSerializer
        elif self.action == 'retrieve':
            return SingleOfferListSerializer
        elif self.action == 'partial_update':
            return OfferWriteSerializer
        elif self.action == 'destroy':
            return SingleOfferListSerializer
        return OfferWriteSerializer  # fallback

    def perform_create(self, serializer):
        # user ist erforderlich und wird nicht im POST JSON mitgesendet, sondern hier!
        serializer.save(user=self.request.user)

    # Einteilung Permissions
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]


# path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(), name='offerdetails-detail'),
class SingleOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer  # hier NICHT die URLS!
    permission_classes = [IsAuthenticated]
