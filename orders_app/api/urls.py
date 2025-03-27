from django.urls import path, include
from .views import PostOrderView, UpdateOrderView, GetOrderCountView, GetCompletedOrderView
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # path('orders/', PostOrderView.as_view(), name='order-post'),
    # path('orders/<int:pk>/', UpdateOrderView.as_view(), name='order-update'),
    path('', include(router.urls)),
    path('order-count/<int:business_user>/',
         GetOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user>/',
         GetCompletedOrderView.as_view(), name='order-completed-count'),
]
