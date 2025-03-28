# Generated by Django 5.1.7 on 2025-03-21 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0005_offer_created_at_offer_updated_at_offer_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='created_at',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='offer',
            name='updated_at',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
