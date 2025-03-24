from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetails, Offer


# Create your models here.


class Order(models.Model):

    ORDER_STATUS_CATEGORIES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    offerdetails = models.OneToOneField(
        OfferDetails, on_delete=models.CASCADE, related_name="related_offerdetails")
    customer_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_user")
    business_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="business_user")
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CATEGORIES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # so wird es angezeigt im backend panel

    def __str__(self):
        return f"{self.customer_user} - {self.business_user}"
