from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet


# urlpatterns = [
#     path('reviews/', ReviewsView.as_view(), name='reviews-list'),
#     path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name='reviews-details'),
# ]


router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
