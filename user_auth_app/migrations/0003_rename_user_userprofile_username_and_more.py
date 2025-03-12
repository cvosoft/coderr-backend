# Generated by Django 5.1.7 on 2025-03-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0002_remove_userprofile_bio_remove_userprofile_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='username',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='description', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='file',
            field=models.FileField(default='default.jpg', upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='first name', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='last name', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default='location', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(default='+49 123456789', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='working_hours',
            field=models.CharField(default='24h', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer'), ('business', 'Business')], default='Customer', max_length=10),
        ),
    ]
