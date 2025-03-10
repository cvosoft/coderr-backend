from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10, choices=USER_TYPES, default='customer')

    # bio = models.TextField(blank=True, null=True)
    # location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"
