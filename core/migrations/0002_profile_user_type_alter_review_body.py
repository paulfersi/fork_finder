# Generated by Django 5.0.6 on 2024-07-05 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("regular", "Regular User"),
                    ("critic", "Culinary Critic"),
                    ("admin", "Admin"),
                ],
                default="regular",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="body",
            field=models.CharField(max_length=255),
        ),
    ]