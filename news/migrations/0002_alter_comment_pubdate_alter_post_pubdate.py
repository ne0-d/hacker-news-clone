# Generated by Django 5.0.2 on 2024-03-13 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pubDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 11, 50, 4, 855212, tzinfo=datetime.timezone.utc), verbose_name='published_date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pubDate',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 11, 50, 4, 854749, tzinfo=datetime.timezone.utc), verbose_name='published_date'),
        ),
    ]
