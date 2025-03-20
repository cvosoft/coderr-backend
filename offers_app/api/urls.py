from django.urls import path
from .views import OffersViewList

urlpatterns = [
    path('offers/', OffersViewList.as_view(), name='offers-list'),
]
