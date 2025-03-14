from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders_app.models import Order
from offers_app.models import OfferDetail
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: Gibt eine Liste aller Bestellungen zurück.
    POST: Erstellt eine neue Bestellung (nur für Kunden erlaubt).
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """ Nur Kunden dürfen Bestellungen erstellen. """

        # Hole den eingeloggten Benutzer
        customer_user = request.user

        # Prüfe, ob der Benutzer ein 'customer' ist
        if hasattr(customer_user, 'userprofile') and customer_user.userprofile.type != "customer":
            return Response(
                {"error": "Nur Kunden können Bestellungen erstellen."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Hole die OfferDetail ID aus dem Request
        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            return Response(
                {"error": "offer_detail_id ist erforderlich."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Hole das entsprechende OfferDetail
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            return Response(
                {"error": "Das angegebene OfferDetail existiert nicht."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Business-User aus dem Offer ermitteln
        business_user = offer_detail.offer.creator

        # Bestellung erstellen
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer_detail=offer_detail
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Gibt die Details einer Bestellung zurück.
    PATCH: Aktualisiert den Status einer Bestellung.
    DELETE: Löscht eine Bestellung.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """ Aktualisiert den Status einer Bestellung. """
        
        order = self.get_object()
        status_value = request.data.get("status")

        # Prüfen, ob der Status gültig ist
        if status_value and status_value in ["in_progress", "completed", "cancelled"]:
            order.status = status_value
            order.save()
            return Response(OrderSerializer(order).data)
        
        return Response(
            {"error": "Ungültiger Status."}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderCountView(generics.RetrieveAPIView):
    """
    GET: Gibt die Anzahl der laufenden Bestellungen für einen Business-User zurück.
    """
    def get(self, request, business_user_id):
        order_count = Order.objects.filter(
            business_user_id=business_user_id, status="in_progress"
        ).count()
        return Response({"order_count": order_count})


class CompletedOrderCountView(generics.RetrieveAPIView):
    """
    GET: Gibt die Anzahl der abgeschlossenen Bestellungen für einen Business-User zurück.
    """
    def get(self, request, business_user_id):
        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id, status="completed"
        ).count()
        return Response({"completed_order_count": completed_order_count})
