# Generated by Django 5.1.7 on 2025-03-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_app', '0006_alter_userprofile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.FileField(default='uploads/profiles/default.jpg', upload_to='uploads/profiles/'),
        ),
    ]
