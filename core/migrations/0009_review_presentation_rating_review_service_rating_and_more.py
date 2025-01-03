# Generated by Django 5.0.6 on 2024-07-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_review_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="presentation_rating",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="service_rating",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="taste_rating",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
