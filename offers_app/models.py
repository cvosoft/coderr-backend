from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Offer(models.Model):
    # manche felder müssen automatisch gesetzt werden, weil ich diese im POST nicht mitsende
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=255)
    image = models.FileField(
        upload_to='uploads/profiles/', null=True, blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    # so wird es angezeigt im backend panel
    def __str__(self):
        return f"{self.title}"


class OfferDetails(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")
    OFFER_DETAIL_CATEGORIES = [
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    title = models.CharField(max_length=255, default="detail titel")
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=255, choices=OFFER_DETAIL_CATEGORIES, default="standard")

    def __str__(self):
        return f"{self.title}"
