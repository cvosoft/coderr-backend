from django.urls import path
from .views import ReviewsView, ReviewsDetailView

urlpatterns = [
    path('reviews/', ReviewsView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name='reviews-details'),
]
