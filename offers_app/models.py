from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/offers/', null=True, blank=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()  # Liste von Features
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"
