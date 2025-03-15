from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path("reviews/", ReviewListView.as_view(), name="review-list"),
    path("reviews/new/", ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<int:pk>/", ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:pk>/delete/",
         ReviewDeleteView.as_view(), name="review-delete"),
]
