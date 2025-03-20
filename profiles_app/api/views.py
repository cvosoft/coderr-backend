from rest_framework import generics
from profiles_app.models import UserProfile
from .serializers import UserProfileSerializer
from .permissions import IsOwnerOrAdmin



class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = "user"


class CustomerProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type='customer')


class BusinessProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')
