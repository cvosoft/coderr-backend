from rest_framework import generics, mixins, status
from orders_app.models import Order
from offers_app.models import OfferDetails
from .serializers import OrderSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


# path('orders/<int:pk>/', UpdateOrderView.as_view(), name='order-update'),
class UpdateOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


# path('orders/', PostOrderView.as_view(), name='order-post'),
class PostOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        offer_detail_id = request.data.get("offer_detail_id")

        if not offer_detail_id:
            return Response({"error": "offer_detail_id fehlt."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            detail = OfferDetails.objects.get(id=offer_detail_id)
        except OfferDetails.DoesNotExist:
            return Response({"error": "OfferDetail nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        # Beispiel: neue Order basierend auf OfferDetail
        print(detail.offer)
        order = Order.objects.create(
            business_user=detail.offer.user,  # nicht creator!!
            customer_user=request.user,
            status="in_progress"
        )

        return Response({
            "message": "Order erfolgreich erstellt.",
            "order_id": order.id,
            "offer_title": detail.offer.title,
            "detail_price": detail.price
        }, status=status.HTTP_201_CREATED)


# path('order-count/<int:pk>/', GetOrderCountView.as_view(), name='order-count')
class GetOrderCountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "order_count": Order.objects.count()
        })


# path('completed-order-count/<int:pk>/', GetCompletedOrderView.as_view(), name='order-completed-count'),
class GetCompletedOrderView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "completed_order_count": Order.objects.count()
        })
