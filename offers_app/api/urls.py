from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


# urlpatterns = [
#     path('offers/', OffersListAllAndPostSingleView.as_view(), name='offers-list'),
#     path('offers/<int:pk>/', SingleOfferView.as_view(), name='offer-single'),
#     path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(), name='offerdetails-detail'),
# ]


router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offers')

urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', SingleOfferDetailView.as_view(),
         name='offerdetails-detail'),
]
