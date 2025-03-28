from rest_framework import generics
from .serializers import ReviewsSerializer, ReviewsPOSTSerializer
from reviews_app.models import Reviews
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated


################
# GET /api/offers/ - list
# POST /api/offers/ - create
# GET /api/offers/{id}/ - retrieve
# PATCH /api/offers/{id}/ - partial update
# DELETE /api/offers/{id}/ - destroy
#################


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Reviews.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    ordering_fields = ['rating', 'updated_at']
    filterset_fields = ['business_user_id', 'reviewer_id']

    # Einteilung Permissions
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [IsCustomerUser()]
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewsSerializer  # Für GET-Anfragen
        return ReviewsPOSTSerializer      # Für POST, PUT, PATCH

    # sorgt dafür dass reviewer id automatisch intern gespeichert wird
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        post_serializer = self.get_serializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        instance = post_serializer.save(reviewer=self.request.user)

        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # nach dem PATCH voller output!
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Nach dem Speichern – Ausgabe mit vollständigem Serializer
        output_serializer = ReviewsSerializer(instance)
        return Response(output_serializer.data)
