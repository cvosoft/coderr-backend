# Generated by Django 5.1.7 on 2025-03-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0004_rename_username_userprofile_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
