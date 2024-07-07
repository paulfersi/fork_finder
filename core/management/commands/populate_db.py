from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant, Review
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', '1234')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))


        user1, created1 = User.objects.get_or_create(username='critic1')
        if created1:
            user1.set_password('password1')
            user1.save()

        user2, created2 = User.objects.get_or_create(username='user2')
        if created2:
            user2.set_password('password2')
            user2.save()

        user3, created3 = User.objects.get_or_create(username='user3')
        if created3:
            user3.set_password('password3')
            user3.save()

        user4, created4 = User.objects.get_or_create(username='user4')
        if created4:
            user4.set_password('password4')
            user4.save()

        user5, created5 = User.objects.get_or_create(username='user5')
        if created5:
            user5.set_password('password5')
            user5.save()

        admin_profile, created_admin_profile = Profile.objects.get_or_create(user=admin_user, defaults={'user_type': 'admin', 'latitude': Decimal('40.712776'), 'longitude': Decimal('-74.005974')})
        if created_admin_profile:
            admin_profile.save()

        profile1, created_profile1 = Profile.objects.get_or_create(user=user1, defaults={'user_type': 'regular', 'latitude': Decimal('40.712776'), 'longitude': Decimal('-74.005974')})
        if created_profile1:
            profile1.save()

        profile2, created_profile2 = Profile.objects.get_or_create(user=user2, defaults={'user_type': 'critic', 'latitude': Decimal('34.052235'), 'longitude': Decimal('-118.243683')})
        if created_profile2:
            profile2.save()

        profile3, created_profile3 = Profile.objects.get_or_create(user=user3, defaults={'user_type': 'regular', 'latitude': Decimal('51.5074'), 'longitude': Decimal('-0.1278')})
        if created_profile3:
            profile3.save()

        profile4, created_profile4 = Profile.objects.get_or_create(user=user4, defaults={'user_type': 'critic', 'latitude': Decimal('48.8566'), 'longitude': Decimal('2.3522')})
        if created_profile4:
            profile4.save()

        profile5, created_profile5 = Profile.objects.get_or_create(user=user5, defaults={'user_type': 'regular', 'latitude': Decimal('37.7749'), 'longitude': Decimal('-122.4194')})
        if created_profile5:
            profile5.save()

        # Add follows relationships

        admin_profile.follows.add(profile1,profile2,profile3,profile4,profile5)
        admin_profile.save()

        profile1.follows.add(profile2, profile3, profile4)
        profile1.save()

        profile2.follows.add(profile1, profile4)
        profile2.save()

        profile3.follows.add(profile1, profile5)
        profile3.save()

        profile4.follows.add(profile2)
        profile4.save()

        profile5.follows.add(profile3, profile4)
        profile5.save()

        restaurant1, created_restaurant1 = Restaurant.objects.get_or_create(place_id='place_id1', defaults={'name': 'Restaurant A', 'address': '123 Main St', 'latitude': '40.712776', 'longitude': '-74.005974'})
        if created_restaurant1:
            restaurant1.save()

        restaurant2, created_restaurant2 = Restaurant.objects.get_or_create(place_id='place_id2', defaults={'name': 'Restaurant B', 'address': '456 Elm St', 'latitude': '34.052235', 'longitude': '-118.243683'})
        if created_restaurant2:
            restaurant2.save()

        restaurant3, created_restaurant3 = Restaurant.objects.get_or_create(place_id='place_id3', defaults={'name': 'Restaurant C', 'address': '789 Oak Ave', 'latitude': '51.5074', 'longitude': '-0.1278'})
        if created_restaurant3:
            restaurant3.save()

        # Create Reviews
        review1, created_review1 = Review.objects.get_or_create(user=user1, restaurant=restaurant1, defaults={'body': 'Great food!', 'rating': 5, 'photo': 'review_photos/photo1.jpg', 'is_featured': True, 'created_at': timezone.now()})
        if created_review1:
            review1.save()

        review2, created_review2 = Review.objects.get_or_create(user=user2, restaurant=restaurant2, defaults={'body': 'Average experience', 'rating': 3, 'photo': 'review_photos/photo2.jpg', 'created_at': timezone.now()})
        if created_review2:
            review2.save()

        review3, created_review3 = Review.objects.get_or_create(user=user3, restaurant=restaurant3, defaults={'body': 'Delicious dishes', 'rating': 4, 'photo': 'review_photos/photo3.jpg', 'created_at': timezone.now()})
        if created_review3:
            review3.save()

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
