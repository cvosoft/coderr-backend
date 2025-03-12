from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="first name")
    last_name = models.CharField(max_length=30, default="last name")
    file = models.FileField(upload_to='uploads/', default="default.jpg")
    location = models.CharField(max_length=30, default="location")
    tel = models.CharField(max_length=30, default = "+49 123456789")
    description = models.CharField(max_length=30, default="description")
    working_hours = models.CharField(max_length=30, default = "24h")
    type = models.CharField(
        max_length=10, choices=USER_TYPES, default='customer')


    def __str__(self):
        return f"{self.user.username} - {self.type}"
