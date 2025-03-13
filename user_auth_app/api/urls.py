from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profile/', UserProfileList.as_view(), name='userprofile-list'),
    path('profile/<int:user>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(),
         name='registration'),
    path('login/', CustomLoginView.as_view(), name='login')
]
