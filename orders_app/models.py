from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetails


# Create your models here.


class Order(models.Model):

    ORDER_STATUS_CATEGORIES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    offerdetails = models.ForeignKey(
        OfferDetails, on_delete=models.CASCADE, related_name="orders")
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_orders")
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_orders")
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CATEGORIES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # so wird es angezeigt im backend panel

    def __str__(self):
        return f"{self.customer_user} - {self.business_user}"
