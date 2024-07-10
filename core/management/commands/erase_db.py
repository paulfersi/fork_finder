from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Restaurant, Review, Profile,User, Permission, Group
import os

class Command(BaseCommand):
    help = 'Erases all database tables and data'

    def handle(self, *args, **options):
        self.stdout.write("Erasing database...")
        for review in Review.objects.all():
            if review.photo:
                if os.path.exists(review.photo.path):
                    os.remove(review.photo.path)
            review.delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Restaurant.objects.all().delete()

        Group.objects.all().delete()
        Permission.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database deleted successfully!'))