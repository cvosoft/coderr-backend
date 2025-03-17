
from django.db.models import Q, Min
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from rest_framework.response import Response


class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]  # Nur eingeloggte User
        return [permissions.AllowAny()]  # GET ist für alle erlaubt

    def get_queryset(self):
        queryset = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )
        request = self.request

        creator_id = request.query_params.get('creator_id')
        if creator_id:
            try:
                creator_id = int(creator_id)
                queryset = queryset.filter(creator__id=creator_id)
            except ValueError:
                pass

        min_price = request.query_params.get('min_price')
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(min_price__gte=min_price)
            except ValueError:
                pass

        max_delivery_time = request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
                queryset = queryset.filter(
                    details__delivery_time_in_days__lte=max_delivery_time
                ).distinct()
            except ValueError:
                pass

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(
                    description__icontains=search_query)
            )

        ordering = request.query_params.get('ordering')
        allowed_ordering_fields = ['updated_at', '-updated_at']

        if ordering in ['min_price', '-min_price']:
            queryset = queryset.order_by(ordering)
        elif ordering in allowed_ordering_fields:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-updated_at')

        return queryset

    def perform_create(self, serializer):
        """
        Speichert ein neues Angebot, falls der Benutzer ein Business-User ist.
        """
        user = self.request.user

        # Prüfen, ob der eingeloggte User ein Business ist
        if not hasattr(user, "userprofile") or user.userprofile.type != "business":
            raise permissions.PermissionDenied(
                "Nur Business-User können Angebote erstellen!"
            )

        # Speichert das Angebot mit dem eingeloggten User als Ersteller
        offer = serializer.save(creator=user)

        # ✅ Gibt `201 Created` mit den erstellten Daten zurück
        return Response(
            OfferSerializer(offer, context={'request': self.request}).data,
            status=201  # `201 Created`
        )


class OfferDetailView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
