from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from reviews_app.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        ordering = self.request.query_params.get("ordering")
        if ordering in ["updated_at", "rating"]:
            queryset = queryset.order_by(f"-{ordering}")

        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user

        if not hasattr(user, "userprofile") or user.userprofile.type != "customer":
            return Response({"error": "Nur Kunden können Bewertungen erstellen."}, status=status.HTTP_403_FORBIDDEN)

        business_user_id = request.data.get("business_user")
        business_user = get_object_or_404(User, id=business_user_id)

        if Review.objects.filter(reviewer=user, business_user=business_user).exists():
            return Response({"error": "Du hast diesen Business bereits bewertet."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=user, business_user=business_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        review = self.get_object()

        # Nur der Ersteller darf bearbeiten
        if review.reviewer != request.user:
            return Response({"error": "Du kannst nur deine eigenen Bewertungen bearbeiten."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()

        # Nur der Ersteller darf löschen
        if review.reviewer != request.user:
            return Response({"error": "Du kannst nur deine eigenen Bewertungen löschen."}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
