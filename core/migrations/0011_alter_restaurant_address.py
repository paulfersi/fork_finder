# Generated by Django 5.0.6 on 2024-07-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_profile_user_type_alter_restaurant_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="address",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
