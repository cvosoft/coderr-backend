from django.urls import path, include
from .views import GetOrderCountView, GetCompletedOrderView
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user>/',
         GetOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user>/',
         GetCompletedOrderView.as_view(), name='order-completed-count'),
]
