from django.urls import path
from .views import UserProfileDetail, CustomerProfileList, BusinessProfileList

urlpatterns = [
    path('profile/<int:user>/', UserProfileDetail.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfileList.as_view(), name='profiles-business-list'),
    path('profiles/customer/', CustomerProfileList.as_view(), name='profiles-customer-list')    
]
