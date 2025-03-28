from rest_framework import generics
from .serializers import ReviewsSerializer, ReviewsPOSTSerializer
from reviews_app.models import Reviews
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.response import Response

# class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer


# class ReviewsView(generics.ListCreateAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewsSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Reviews.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    ordering_fields = ['rating', 'updated_at']
    filterset_fields = ['business_user_id', 'reviewer_id']

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
