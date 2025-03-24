from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Reviews(models.Model):

    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_given")
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_gotten")
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
