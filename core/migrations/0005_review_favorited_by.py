# Generated by Django 5.0.6 on 2024-07-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_profile_latitude_profile_longitude"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="favorited_by",
            field=models.ManyToManyField(
                blank=True, related_name="favorite_reviews", to="core.profile"
            ),
        ),
    ]
