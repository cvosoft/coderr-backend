from django.urls import path
from .views import PostOrderView, UpdateOrderView, GetOrderCountView, GetCompletedOrderView

urlpatterns = [
    path('orders/', PostOrderView.as_view(), name='order-post'),
    path('orders/<int:pk>/', UpdateOrderView.as_view(), name='order-update'),
    path('order-count/<int:pk>/',
         GetOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/',
         GetCompletedOrderView.as_view(), name='order-completed-count'),
]
