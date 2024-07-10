from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from .models import Profile, Review, Restaurant
from django.contrib.contenttypes.models import ContentType

class ReviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.regular_user = User.objects.create_user(username='regularuser', password='password')
        self.critic_user = User.objects.create_user(username='criticuser', password='password')
        
        self.regular_group = Group.objects.create(name="Regular")
        self.critic_group = Group.objects.create(name="Critics")
        

        self.regular_user.groups.add(self.regular_group)
        self.critic_user.groups.add(self.critic_group)
        

        Profile.objects.create(user=self.regular_user, user_type='regular')
        Profile.objects.create(user=self.critic_user, user_type='critic')
        

        content_type = ContentType.objects.get_for_model(Review)
        self.can_write_featured_review = Permission.objects.create(
            codename='can_write_featured_review',
            name='Can write featured review',
            content_type=content_type,
        )
        

        self.critic_group.permissions.add(self.can_write_featured_review)
        
        self.restaurant = Restaurant.objects.create(
            place_id="1234", name="Test Restaurant", address="123 Street", latitude="0.000000", longitude="0.000000"
        )

    def test_regular_user_cannot_add_featured_review(self):
        #user cannot write a pro review
        self.client.login(username='regularuser', password='password')
        response = self.client.post(reverse('add_pro_review'), {
            'body': 'Test review body',
            'rating': 5,
            'taste_rating': 4,
            'presentation_rating': 4,
            'service_rating': 4,
            'restaurant': self.restaurant.id,
        })
        self.assertEqual(response.status_code, 403)  

    def test_add_to_favorites(self):
        self.client.login(username='regularuser', password='password')

        review = Review.objects.create(
            user=self.critic_user,
            restaurant=self.restaurant,
            body="Great food!",
            rating=5
        )

        response = self.client.post(reverse('feed'), {
            'review_id': review.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(review, self.regular_user.profile.favorite_reviews.all())

    def test_review_added_to_database(self):
        self.client.login(username='regularuser', password='password')
        response = self.client.post(reverse('add_review'), {
            'body': 'Test review body',
            'rating': 5,
            'restaurant': self.restaurant.id,
        })
        
        self.assertEqual(response.status_code, 200)
        

        self.assertTrue(Review.objects.filter(body='Test review body', user=self.regular_user).exists())

    def test_critic_user_permission(self):
        self.assertTrue(self.critic_user.groups.filter(name='Critics').exists())
        self.assertEqual(self.critic_user.profile.user_type, 'critic')
        self.assertTrue(self.critic_user.has_perm('core.can_write_featured_review'))

    def test_regular_user_permission(self):
        self.assertTrue(self.regular_user.groups.filter(name='Regular').exists())
        self.assertEqual(self.regular_user.profile.user_type, 'regular')
        self.assertFalse(self.regular_user.has_perm('core.can_write_featured_review'))
