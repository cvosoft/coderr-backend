# Generated by Django 5.1.7 on 2025-03-22 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0009_alter_offerdetails_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetails',
            name='features',
            field=models.JSONField(default=list),
        ),
    ]
