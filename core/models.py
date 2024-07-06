from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        if instance.profile != user_profile:
            user_profile.follows.add(instance.profile)
            user_profile.save()

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('critic', 'Culinary Critic'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    favorite_reviews = models.ManyToManyField('Review', related_name='favorited_by_profiles', blank=True)

    def __str__(self):
        return self.user.username

    def is_culinary_critic(self):
        return self.user_type == 'critic'

class Restaurant(models.Model):
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=120)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.location}"

class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='media/review_photos/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("mark_featured_review", "Can mark a review as featured"),
        ]

    def __str__(self):
        return f"{self.user} {self.restaurant.name} ({self.created_at:%Y-%m-%d %H:%M}): "
