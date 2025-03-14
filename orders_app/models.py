from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetail


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_orders')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.offer_detail.title} ({self.status})"
