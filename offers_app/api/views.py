from django.db.models import Q, Min
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer, OfferDetailURLSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

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
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
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
        """ Speichert ein neues Angebot mit Details, falls der Benutzer ein Business-User ist. """
        user = self.request.user

        if not hasattr(user, "userprofile") or user.userprofile.type != "business":
            raise PermissionDenied("Nur Business-User können Angebote erstellen!")

        offer = serializer.save(creator=user)

        return Response(
            OfferSerializer(offer, context={'request': self.request}).data,
            status=status.HTTP_201_CREATED
        )


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        offer = super().get_object()

        if self.request.method in ["PATCH", "DELETE"] and offer.creator != self.request.user:
            raise PermissionDenied("Nur der Ersteller kann dieses Angebot ändern oder löschen!")

        return offer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """ Gibt die vollständigen OfferDetail-Daten zurück """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer  # Korrekte Nutzung des Serializers
