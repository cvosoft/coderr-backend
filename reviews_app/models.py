from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    business_user = models.ForeignKey(
        User, related_name="reviews_received", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, related_name="reviews_written", on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ein Kunde kann einen Business nur einmal bewerten
        unique_together = ('business_user', 'reviewer')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Review {self.id} - {self.reviewer} -> {self.business_user}"
