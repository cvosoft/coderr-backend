from rest_framework import generics, mixins
from offers_app.models import Offer, OfferDetails
from .serializers import SingleOfferListSerializer, OfferWriteSerializer, OffersListSerializer, OfferDetailSerializer, OfferDetailURLSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import ResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter
from .permissions import IsBusinessUser, IsOwnerOrAdmin


# für gesamtliste und fürs posten
# path('offers/', OffersListAllAndPostSingleView.as_view(), name='offers-list'),
class OffersListAllAndPostSingleView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    # permission_classes = [AllowAny]
    pagination_class = ResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    # unterschiedliche serializer für listenview und singlepost

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OffersListSerializer
        # bei POST
        return OfferWriteSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # user ist erforderlich und wird nicht im POST JSON mitgesendet, sondern hier!
        serializer.save(user=self.request.user)


# path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(), name='offerdetails-detail'),
class SingleOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer  # hier NICHT die URLS!
    permission_classes = [IsAuthenticated]


# path('offers/<int:pk>/', SingleOfferView.as_view(), name='offer-single'),
# RetrieveUpdateDestroyAPIView -> für Detailansichten!
# get, put, patch, delete ist da mit drin!
class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = SingleOfferListSerializer
    permission_classes = [IsAuthenticated]


