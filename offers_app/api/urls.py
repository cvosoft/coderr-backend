from django.urls import path
from .views import OfferList, OfferDetail


urlpatterns = [
    path('offers/', OfferList.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetail.as_view(),
         name='offer-detail'),
]
