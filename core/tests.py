from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Review, Restaurant
import json
from django.core.exceptions import ValidationError
from .utils import get_recommended_reviews

class FeedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_feed_view_access(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_add_to_favorite(self):
        restaurant = Restaurant.objects.create(place_id='123', name='Test Restaurant', latitude='123.456', longitude='456.789')
        review = Review.objects.create(user=self.user, restaurant=restaurant, body='Test Review', rating=5)
        profile = Profile.objects.get(user=self.user)
        profile.favorite_reviews.add(review)

        response = self.client.post(reverse('feed'), {'review_id': review.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        favorite_review_ids = list(profile.favorite_reviews.values_list('id', flat=True))
        self.assertIn(review.id, favorite_review_ids)


class AddReviewViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_add_review_get(self):
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_review.html')

    def test_add_review_post(self):
        restaurant_data = {
            'place_id': '123',
            'name': 'Test Restaurant',
            'latitude': '123.456',
            'longitude': '456.789',
        }

        response = self.client.post(reverse('add_review'), {
            'selected_place': json.dumps(restaurant_data),
            'body': 'Test Review',
            'rating': 5,
        })

        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Restaurant.objects.count(), 1)


class ReviewModelTestCase(TestCase):
    def setUp(self):

        self.regular_user = User.objects.create_user(username='regularuser', password='12345')
        self.regular_profile = Profile.objects.create(user=self.regular_user, user_type='regular')

 
        self.critic_user = User.objects.create_user(username='criticuser', password='12345')
        self.critic_profile = Profile.objects.create(user=self.critic_user, user_type='critic')


        self.restaurant = Restaurant.objects.create(place_id='123', name='Test Restaurant', latitude='123.456', longitude='456.789')

    def test_only_culinary_critic_can_write_featured_review(self):

        with self.assertRaises(ValidationError) as cm:
            review = Review.objects.create(
                user=self.regular_user,
                restaurant=self.restaurant,
                body='Test Review',
                rating=5,
                is_featured=True
            )
        self.assertIn("Only culinary critics can write featured reviews", str(cm.exception))

        try:
            review = Review.objects.create(
                user=self.critic_user,
                restaurant=self.restaurant,
                body='Test Review',
                rating=5,
                is_featured=True
            )
        except ValidationError:
            self.fail("Culinary critic should be able to write featured reviews.")


