from django.db import models

# Create your models here.


class Order(models.Model):

    customer_user = models.CharField(max_length=255)
    business_user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    revisions = models.CharField(max_length=255)
    delivery_time_in_days = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    features = models.CharField(max_length=255)
    offer_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)
    updated_at = models.CharField(max_length=255)

    # so wird es angezeigt im backend panel

    def __str__(self):
        return f"{self.customer_user} - {self.business_user}"
