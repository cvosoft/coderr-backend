from django.db import models


# Create your models here.


class Offer(models.Model):

    title = models.CharField(max_length=255)
    image = models.FileField(
        upload_to='uploads/profiles/', null=True, blank=True)
    description = models.CharField(max_length=255)

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
    revisions = models.IntegerField
    delivery_time_in_days = models.IntegerField
    price = models.FloatField
    features = models.JSONField
    offer_type = models.CharField(
        max_length=255, choices=OFFER_DETAIL_CATEGORIES, default="standard")

    def __str__(self):
        return f"{self.title}"
