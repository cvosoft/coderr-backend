from django.urls import path
from .views import UserProfileList, UserProfileDetail, CustomerProfileList, BusinessProfileList


urlpatterns = [
    path('profiles/business/', BusinessProfileList.as_view(),
         name='userprofiles-business-list'),
    path('profiles/customer/', CustomerProfileList.as_view(),
         name='userprofiles-customer-list'),
    path('profile/<int:user>/', UserProfileDetail.as_view(),
         name='userprofile-detail'),
]
