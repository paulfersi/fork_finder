import csv
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from core.models import Profile, Restaurant, Review

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        Profile.objects.all().delete()
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        Review.objects.all().delete()

        # Create users with random profiles
        users = []
        for i in range(5):
            username = fake.user_name()
            email = fake.email()
            password = "password"
            user = User.objects.create_user(username=username, email=email, password=password)
            user.profile.save()
            users.append(user)

        # Read restaurants from CSV and create them
        with open('restaurants.csv', 'r') as file:
            reader = csv.DictReader(file)
            restaurants = []
            for row in reader:
                restaurant = Restaurant.objects.create(
                    place_id=row['place_id'],
                    name=row['name'],
                    location=row['location']
                )
                restaurants.append(restaurant)

        # Create reviews with random content
        for user in users:
            for restaurant in restaurants:
                body = "Lorem ipsum dolor sit amet, consectetur adipisci elit,\
                        sed do eiusmod tempor incidunt ut labore et dolore magna aliqua."
                rating = random.randint(1, 5)
                review = Review.objects.create(user=user, restaurant=restaurant, body=body, rating=rating, photo=None)

        # Link users to follow each other (simple example: each user follows the next one)
        for i, user in enumerate(users):
            profile = user.profile
            profile.follows.add(users[(i+1) % len(users)].profile)
            profile.save()

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
