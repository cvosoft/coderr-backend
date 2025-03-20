from django.db import models


# Create your models here.


class Offer(models.Model):

    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/profiles/')
    description = models.CharField(max_length=255)

    # so wird es angezeigt im backend panel
    def __str__(self):
        return f"{self.title}"
