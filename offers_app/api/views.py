from django.db.models import Q, Min
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from offers_app.models import Offer
from .serializers import OfferSerializer


class OfferPagination(PageNumberPagination):
    page_size = 10  # Standard 10 Einträge pro Seite
    page_size_query_param = 'page_size'  # Ermöglicht `?page_size=20`
    max_page_size = 100  # Max. Einträge pro Seite


class OfferListView(generics.ListAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_queryset(self):
        queryset = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )
        request = self.request

        # Filter nach creator_id (falls vorhanden)
        creator_id = request.query_params.get('creator_id')
        if creator_id:
            try:
                creator_id = int(creator_id)
                queryset = queryset.filter(creator__id=creator_id)
            except ValueError:
                pass  # Falls keine Zahl, ignorieren

        # Filter nach min_price
        min_price = request.query_params.get('min_price')
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(min_price__gte=min_price)
            except ValueError:
                pass

        # Filter nach max_delivery_time
        max_delivery_time = request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
                queryset = queryset.filter(
                    details__delivery_time_in_days__lte=max_delivery_time
                ).distinct()
            except ValueError:
                pass

        # Suche in title und description
        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Sortierung (ordering)
        ordering = request.query_params.get('ordering')
        allowed_ordering_fields = ['updated_at', '-updated_at']

        if ordering in ['min_price', '-min_price']:
            queryset = queryset.order_by(ordering)
        elif ordering in allowed_ordering_fields:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-updated_at')  # Standard: Neuste zuerst

        return queryset


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
