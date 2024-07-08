from django.db import models
from django.contrib.auth.models import User, Permission, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_culinary_critic():
            group, created = Group.objects.get_or_create(name='Critics')
            self.user.groups.add(group)
            content_type = ContentType.objects.get_for_model(Review)
            permission, created = Permission.objects.get_or_create(
                codename='can_write_featured_review',
                name='Can write featured review',
                content_type=content_type,
            )
            group.permissions.add(permission)
        else:
            group = Group.objects.filter(name='Critics').first()
            if group:
                self.user.groups.remove(group)


class Restaurant(models.Model):
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=120,blank=True,null=True)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} | {self.address}"

class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()

    # specific to culinary critics
    taste_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    presentation_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    service_rating = models.PositiveSmallIntegerField(blank=True, null=True)

    photo = models.ImageField(upload_to='media/review_photos/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.restaurant.name} ({self.created_at:%Y-%m-%d %H:%M}) "
    
    def save(self, *args, **kwargs):
        if self.is_featured:
            if not self.user.has_perm('app.can_write_featured_review'):
                raise ValueError("Only culinary critics can write featured reviews")
        
        super().save(*args, **kwargs)


