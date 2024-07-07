from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant, Review
from decimal import Decimal
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        admin_username = 'admin'
        admin_password = '1234'
        admin_email = 'admin@example.com'

        admin_user = User.objects.filter(username=admin_username).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(admin_username, admin_email, admin_password)
            self.stdout.write(self.style.SUCCESS('Superuser "{}" created successfully'.format(admin_username)))
        else:
            self.stdout.write(self.style.WARNING('Superuser "{}" already exists'.format(admin_username)))

        users_data = [
            {
                'username': 'diego',
                'password': 'diegopass',
                'email': 'diego@example.com',
                'user_type': 'regular',
                'city': 'Madrid',
                'latitude': Decimal('40.4168'),
                'longitude': Decimal('-3.7038')
            },
            {
                'username': 'elena',
                'password': 'elenapass',
                'email': 'elena@example.com',
                'user_type': 'critic',
                'city': 'Madrid',
                'latitude': Decimal('40.4172'),
                'longitude': Decimal('-3.7042')
            },
            {
                'username': 'pierre',
                'password': 'pierrepass',
                'email': 'pierre@example.com',
                'user_type': 'regular',
                'city': 'Paris',
                'latitude': Decimal('48.8566'),
                'longitude': Decimal('2.3522')
            },
            {
                'username': 'sophie',
                'password': 'sophiepass',
                'email': 'sophie@example.com',
                'user_type': 'critic',
                'city': 'Paris',
                'latitude': Decimal('48.8584'),
                'longitude': Decimal('2.2945')
            },
            {
                'username': 'giuseppe',
                'password': 'giuseppepass',
                'email': 'giuseppe@example.com',
                'user_type': 'regular',
                'city': 'Modena',
                'latitude': Decimal('44.6475'),
                'longitude': Decimal('10.9254')
            },
            {
                'username': 'anna',
                'password': 'annapass',
                'email': 'anna@example.com',
                'user_type': 'critic',
                'city': 'Modena',
                'latitude': Decimal('44.6488'),
                'longitude': Decimal('10.9215')
            },
            {
                'username': 'maximilian',
                'password': 'maximilianpass',
                'email': 'maximilian@example.com',
                'user_type': 'regular',
                'city': 'Berlin',
                'latitude': Decimal('52.5200'),
                'longitude': Decimal('13.4050')
            },
            {
                'username': 'sophia',
                'password': 'sophiapass',
                'email': 'sophia@example.com',
                'user_type': 'critic',
                'city': 'Berlin',
                'latitude': Decimal('52.5233'),
                'longitude': Decimal('13.4127')
            },
        ]

        restaurants_data = [
            {
                'place_id': 'place_id4',
                'name': 'Osteria Francescana',
                'address': '12 Modena St',
                'latitude': Decimal('44.644'),
                'longitude': Decimal('10.9254')
            },
            {
                'place_id': 'place_id5',
                'name': 'Trattoria Aldina',
                'address': '23 Via Giuseppe Mazzini',
                'latitude': Decimal('44.6478'),
                'longitude': Decimal('10.9265')
            },
            {
                'place_id': 'place_id6',
                'name': 'Le Grand Véfour',
                'address': '17 Rue de Beaujolais',
                'latitude': Decimal('48.8658'),
                'longitude': Decimal('2.337')
            },
            {
                'place_id': 'place_id7',
                'name': 'L\'Astrance',
                'address': '4 Rue Beethoven',
                'latitude': Decimal('48.8587'),
                'longitude': Decimal('2.2909')
            },
            {
                'place_id': 'place_id8',
                'name': 'Rutz',
                'address': 'Chausseestraße 8',
                'latitude': Decimal('52.5311'),
                'longitude': Decimal('13.3841')
            },
            {
                'place_id': 'place_id9',
                'name': 'Pauly Saal',
                'address': 'Auguststraße 11-13',
                'latitude': Decimal('52.5287'),
                'longitude': Decimal('13.4022')
            },
            {
                'place_id': 'place_id10',
                'name': 'Sobrino de Botín',
                'address': 'Calle de Cuchilleros 17',
                'latitude': Decimal('40.4144'),
                'longitude': Decimal('-3.708')
            },
            {
                'place_id': 'place_id11',
                'name': 'Casa Lucio',
                'address': 'Calle Cava Baja 35',
                'latitude': Decimal('40.4125'),
                'longitude': Decimal('-3.7071')
            },
        ]

        reviews_data = [
            {'body': 'Excellent food and service!', 'rating': 5, 'photo': 'review_photos/photo1.jpg', 'is_featured': False},
            {'body': 'Decent place, good ambiance.', 'rating': 4, 'photo': 'review_photos/photo2.jpg', 'is_featured': False},
            {'body': 'The food was okay, service could be better.', 'rating': 3, 'photo': 'review_photos/photo3.jpg', 'is_featured': False},
            {'body': 'Amazing experience, will visit again!', 'rating': 5, 'photo': 'review_photos/photo4.jpg', 'is_featured': False},
            {'body': 'Disappointing, food quality was poor.', 'rating': 2, 'photo': 'review_photos/photo5.jpg', 'is_featured': False},
            {'body': 'Lovely place, great for special occasions.', 'rating': 4, 'photo': 'review_photos/photo6.jpg', 'is_featured': False},
            {'body': 'Average food, nothing exceptional.', 'rating': 3, 'photo': 'review_photos/photo7.jpg', 'is_featured': False},
            {'body': 'Best restaurant in town, highly recommended!', 'rating': 5, 'photo': 'review_photos/photo8.jpg', 'is_featured': False},
            {'body': 'Overpriced for the quality offered.', 'rating': 2, 'photo': 'review_photos/photo9.jpg', 'is_featured': False},
        ]

        # Populate users and profiles
        for user_data in users_data:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            user_type = user_data['user_type']
            city = user_data['city']
            latitude = user_data['latitude']
            longitude = user_data['longitude']

            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()

            # Use username as profile name
            profile, created = Profile.objects.get_or_create(user=user, defaults={'user_type': user_type, 'latitude': latitude, 'longitude': longitude, 'name': username})
            if created:
                profile.save()

        # Populate restaurants
        for restaurant_data in restaurants_data:
            place_id = restaurant_data['place_id']
            name = restaurant_data['name']
            address = restaurant_data['address']
            latitude = restaurant_data['latitude']
            longitude = restaurant_data['longitude']

            restaurant, created = Restaurant.objects.get_or_create(place_id=place_id, defaults={'name': name, 'address': address, 'latitude': latitude, 'longitude': longitude})
            if created:
                restaurant.save()

        # Create reviews
        for user_data in users_data:
            user = User.objects.get(username=user_data['username'])
            random_restaurant = random.choice(restaurants_data)
            restaurant = Restaurant.objects.get(place_id=random_restaurant['place_id'])
            random_review = random.choice(reviews_data)

            review_body = random_review['body']
            review_rating = random_review['rating']
            review_photo = random_review['photo'] if 'photo' in random_review else None
            review_is_featured = random_review['is_featured']

            review, created = Review.objects.get_or_create(user=user, restaurant=restaurant, defaults={'body': review_body, 'rating': review_rating, 'photo': review_photo, 'is_featured': review_is_featured, 'created_at': timezone.now()})
            if created:
                review.save()

        self.stdout.write(self.style.SUCCESS('Database populated successfully with reviews!'))
