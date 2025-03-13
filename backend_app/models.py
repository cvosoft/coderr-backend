from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)  # Neu hinzugefügt
    email = models.EmailField(max_length=255, blank=True)  # Neu hinzugefügt
    first_name = models.CharField(max_length=30, default="first name")
    last_name = models.CharField(max_length=30, default="last name")
    file = models.FileField(upload_to='uploads/', default="default.jpg")
    location = models.CharField(max_length=30, default="location")
    tel = models.CharField(max_length=30, default="+49 123456789")
    description = models.CharField(max_length=30, default="description")
    working_hours = models.CharField(max_length=30, default="24h")
    type = models.CharField(
        max_length=10, choices=USER_TYPES, default='customer')
    created_at = models.DateTimeField(default=now)  # Neu hinzugefügt

    def save(self, *args, **kwargs):
        if self.user:
            self.username = self.user.username  # Username übernehmen
            self.email = self.user.email  # E-Mail aus dem User übernehmen
            self.first_name = self.user.first_name  # Optional: First Name übernehmen
            self.last_name = self.user.last_name  # Optional: Last Name übernehmen
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.type}"
