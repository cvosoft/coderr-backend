from django.urls import path
from .views import ReviewListCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path("reviews/", ReviewListCreateView.as_view(), name="review-list-create"),  # ERSETZT ReviewListView & ReviewCreateView
    path("reviews/<int:pk>/", ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review-delete"),
]
