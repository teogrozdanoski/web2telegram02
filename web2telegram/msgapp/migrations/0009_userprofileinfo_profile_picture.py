# Generated by Django 4.1.2 on 2022-10-15 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgapp', '0008_userprofileinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]