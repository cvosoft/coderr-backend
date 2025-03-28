from rest_framework import generics
from profiles_app.models import UserProfile
from .serializers import UserProfileSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = "user"


class CustomerProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return UserProfile.objects.filter(type='customer')


class BusinessProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')
