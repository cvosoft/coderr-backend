from rest_framework import generics, mixins, status
from orders_app.models import Order
from offers_app.models import OfferDetails
from profiles_app.models import UserProfile
from .serializers import *
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action


class GetOrderCountView(APIView):
    permission_classes = [IsAuthUser]

    def get(self, request, business_user):  # wird in der url übergeben
        # abfangen wenn kein business_user
        try:
            profile = UserProfile.objects.get(user__id=business_user)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile wurde nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        if profile.type != "business":
            return Response({"error": "Kein Business-User."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(
            business_user=business_user, status="in_progress").count()
        return Response({
            "order_count": count
        })


class GetCompletedOrderView(APIView):
    permission_classes = [IsAuthUser]

    def get(self, request, business_user):  # wird in der url übergeben
        count = Order.objects.filter(
            business_user=business_user, status="completed").count()
        return Response({
            "completed_order_count": count
        })

################
# GET /api/offers/ - list
# POST /api/offers/ - create
# GET /api/offers/{id}/ - retrieve
# PATCH /api/offers/{id}/ - partial update
# DELETE /api/offers/{id}/ - destroy
#################


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsCustomerUser()]
        if self.action in ['destroy']:
            return [IsAdminUser()]
        if self.action in ['partial_update']:
            return [IsBusinessUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Überschreibt create, um benutzerdefiniertes Response-Objekt zu liefern"""
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)
