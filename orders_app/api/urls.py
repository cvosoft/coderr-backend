from django.urls import path
from .views import

urlpatterns = [
    path('orders/', OffersListAllAndPostSingleView.as_view(), name='orders-list'),
    path('order-count/<pk>/',
         OffersListAllAndPostSingleView.as_view(), name='orders-list'),
    path('completed-order-count/<pk>/',
         OffersListAllAndPostSingleView.as_view(), name='orders-list'),
]
