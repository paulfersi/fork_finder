from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Restaurant, Review, Profile,User

class Command(BaseCommand):
    help = 'Erases all database tables and data'

    def handle(self, *args, **options):
        self.stdout.write("Erasing database...")
        Review.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database deleted successfully!'))