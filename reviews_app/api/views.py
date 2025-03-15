from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from reviews_app.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListView(generics.ListAPIView):
    """
    GET: Listet alle Bewertungen auf. Unterstützt Filter und Sortierung.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Review.objects.all()

        # Filter nach Business-User-ID
        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        # Filter nach Reviewer-ID
        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        # Sortierung nach 'updated_at' oder 'rating'
        ordering = self.request.query_params.get("ordering")
        if ordering in ["updated_at", "rating"]:
            queryset = queryset.order_by(f"-{ordering}")

        return queryset


class ReviewCreateView(generics.CreateAPIView):
    """
    POST: Erstellt eine neue Bewertung. Nur Kunden dürfen bewerten.
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        # Prüfe, ob der Benutzer ein Kunde ist
        if not hasattr(user, "userprofile") or user.userprofile.type != "customer":
            return Response({"error": "Nur Kunden können Bewertungen erstellen."}, status=status.HTTP_403_FORBIDDEN)

        # Prüfe, ob der Benutzer diesen Business schon bewertet hat
        business_user_id = request.data.get("business_user")
        if Review.objects.filter(reviewer=user, business_user_id=business_user_id).exists():
            return Response({"error": "Du hast diesen Business bereits bewertet."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewUpdateView(generics.UpdateAPIView):
    """
    PATCH: Aktualisiert eine bestehende Bewertung (nur 'rating' und 'description').
    """
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
    """
    DELETE: Löscht eine Bewertung (nur der Ersteller kann löschen).
    """
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()

        # Nur der Ersteller darf löschen
        if review.reviewer != request.user:
            return Response({"error": "Du kannst nur deine eigenen Bewertungen löschen."}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
