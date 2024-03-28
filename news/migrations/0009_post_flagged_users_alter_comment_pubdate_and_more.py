# Generated by Django 5.0.2 on 2024-03-18 06:33

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0008_alter_comment_pubdate_alter_post_pubdate"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="flagged_users",
            field=models.ManyToManyField(
                blank=True, related_name="flagged_posts", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="pubDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 6, 33, 51, 283360, tzinfo=datetime.timezone.utc
                ),
                verbose_name="published_date",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pubDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 6, 33, 51, 282591, tzinfo=datetime.timezone.utc
                ),
                verbose_name="published_date",
            ),
        ),
    ]
