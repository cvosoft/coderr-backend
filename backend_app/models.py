from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30, blank=True, default="")
    last_name = models.CharField(max_length=30, blank=True, default="")
    file = models.FileField(upload_to='uploads/', default="default.jpg")
    location = models.CharField(max_length=30, blank=True, default="")
    tel = models.CharField(max_length=30, blank=True, default="")
    description = models.CharField(max_length=30, blank=True, default="")
    working_hours = models.CharField(max_length=30, blank=True, default="")
    type = models.CharField(
        max_length=10, choices=USER_TYPES, default='customer')
    created_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if self.user:
            self.username = self.user.username  # Username übernehmen
            self.email = self.user.email  # E-Mail aus dem User übernehmen
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.type}"
