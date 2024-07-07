# Generated by Django 5.0.6 on 2024-07-07 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_review_presentation_rating_review_service_rating_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user_type",
            field=models.CharField(
                choices=[("regular", "Regular User"), ("critic", "Culinary Critic")],
                default="regular",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="address",
            field=models.CharField(blank=True, max_length=120),
        ),
    ]