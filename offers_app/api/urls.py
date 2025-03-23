from django.urls import path
from .views import SingleOfferView, OffersListAllAndPostSingleView, SingleOfferDetailView

urlpatterns = [
    path('offers/', OffersListAllAndPostSingleView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', SingleOfferView.as_view(), name='offer-single'),
    path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(), name='offerdetails-detail'),
]
