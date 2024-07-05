from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username

class Restaurant(models.Model):  
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=60)  
    address = models.CharField(max_length=120)  
    longitude = models.CharField(max_length=255)  
    latitude = models.CharField(max_length=255)    

    def __str__(self):
        return (
            f"{self.name} "
            f"{self.location}"
        )
    
class Review(models.Model):
    user= models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    rating = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='media/review_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"{self.restaurant.name} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
        )