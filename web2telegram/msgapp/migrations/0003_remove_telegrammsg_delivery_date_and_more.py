# Generated by Django 4.1.2 on 2022-10-09 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgapp', '0002_alter_recipient_telegram_id_alter_recipient_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrammsg',
            name='delivery_date',
        ),
        migrations.RemoveField(
            model_name='telegrammsg',
            name='read_date',
        ),
        migrations.AlterField(
            model_name='telegrammsg',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 9, 21, 27, 0, 372255)),
        ),
    ]