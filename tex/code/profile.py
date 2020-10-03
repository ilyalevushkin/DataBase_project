from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .favourites import Favourites

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank = True)
    photo = models.ImageField(
        upload_to='img/profiles',
        default='img/profiles/base_profile.jpg'
    )
    favourite = models.OneToOneField(Favourites,
                                     on_delete = models.PROTECT,
                                     null=True, blank = True)
    about = models.TextField(blank = True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()