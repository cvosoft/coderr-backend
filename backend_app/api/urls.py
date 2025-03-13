from django.urls import path
from .views import UserProfileList, UserProfileDetail


urlpatterns = [
    path('profile/', UserProfileList.as_view(), name='userprofile-list'),
    path('profile/<int:user>/', UserProfileDetail.as_view(), name='userprofile-detail'),
]
